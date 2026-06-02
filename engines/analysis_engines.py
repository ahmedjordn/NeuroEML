"""
NeuroEML Analysis Engines
Core analysis engines: Identity Engine, Header Engine, URL Engine
"""

import re
import socket
import logging
import requests
import concurrent.futures
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse, unquote
import idna

logger = logging.getLogger(__name__)

class IdentityEngine:
    @staticmethod
    def detect_punycode(domain: str) -> Dict:
        result = {'is_punycode': False, 'original': domain, 'decoded': domain, 'is_suspicious': False, 'suspicious_chars': []}
        if not domain or not isinstance(domain, str): return result
        try:
            if domain.startswith('xn--'):
                result['is_punycode'] = True
                decoded = idna.decode(domain)
                result['decoded'] = decoded
                for char in decoded:
                    if ord(char) > 127:
                        result['suspicious_chars'].append(char)
                        result['is_suspicious'] = True
        except Exception as e:
            logger.warning(f"Failed to decode Punycode {domain}: {e}")
        return result

    @staticmethod
    def extract_email_address(from_header: str) -> Tuple[str, str, str]:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+'
        display_name, email_address, domain = "", "", ""
        try:
            email_match = re.search(email_pattern, from_header)
            if email_match:
                email_address = email_match.group(0)
                domain = email_address.split('@')[1]
            if '<' in from_header:
                display_name = from_header[:from_header.index('<')].strip().strip('"\'')
            else:
                display_name = re.sub(email_pattern, '', from_header).strip().strip('"\'')
        except Exception as e:
            logger.warning(f"Failed to parse From header: {e}")
        return display_name, email_address, domain

    @staticmethod
    def check_homograph_attack(display_name: str, email_address: str) -> Dict:
        result = {'is_spoofing_attempt': False, 'display_name': display_name, 'actual_email': email_address, 'risk_score': 0, 'indicators': []}
        if not display_name or not email_address: return result
        
        display_lower, email_lower = display_name.lower(), email_address.lower()
        brands = ['apple', 'microsoft', 'google', 'amazon', 'paypal', 'bank', 'irs', 'noreply']
        
        for brand in brands:
            if brand in display_lower and brand not in email_lower:
                result['is_spoofing_attempt'] = True
                result['risk_score'] += 20
                result['indicators'].append(f"Display name contains '{brand}' but email doesn't")
                
        if len(display_name) > len(email_address) * 0.5:
            if not any(word in email_lower for word in display_lower.split()):
                result['is_spoofing_attempt'] = True
                result['risk_score'] += 15
                result['indicators'].append("Display name doesn't match email domain")
        return result

    @classmethod
    def analyze(cls, from_header: str) -> Dict:
        display_name, email_address, domain = cls.extract_email_address(from_header)
        analysis = {
            'from_header': from_header, 'display_name': display_name, 'email_address': email_address,
            'domain': domain, 'punycode_check': cls.detect_punycode(domain),
            'homograph_check': cls.check_homograph_attack(display_name, email_address)
        }
        analysis['risk_score'] = analysis['punycode_check'].get('is_suspicious', False) * 30 + analysis['homograph_check'].get('risk_score', 0)
        return analysis

class HeaderEngine:
    @staticmethod
    def extract_auth_results(auth_results_header: str) -> Dict:
        result = {'raw': auth_results_header, 'spf': {'status': 'none', 'domain': None}, 'dkim': {'status': 'none', 'domain': None}, 'dmarc': {'status': 'none', 'domain': None}}
        if not auth_results_header: return result
        try:
            spf_match = re.search(r'spf=(\w+)\s+\(([^)]+)\)\s+smtp.mailfrom=([^\s;]+)', auth_results_header)
            if spf_match: result['spf'] = {'status': spf_match.group(1), 'domain': spf_match.group(3)}
            
            dkim_match = re.search(r'dkim=(\w+)\s+\(([^)]+)\)\s+header.d=([^\s;]+)', auth_results_header)
            if dkim_match: result['dkim'] = {'status': dkim_match.group(1), 'domain': dkim_match.group(3)}
            
            dmarc_match = re.search(r'dmarc=(\w+)\s+\(([^)]+)\)\s+header.from=([^\s;]+)', auth_results_header)
            if dmarc_match: result['dmarc'] = {'status': dmarc_match.group(1), 'domain': dmarc_match.group(3)}
        except Exception as e:
            logger.warning(f"Failed to parse auth results: {e}")
        return result

    @staticmethod
    def reverse_dns_lookup(ip: str) -> Optional[str]:
        try: return socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.gaierror): return None

    @classmethod
    def analyze(cls, headers: Dict, received_chain: List[Dict]) -> Dict:
        analysis = {'authentication': cls.extract_auth_results(headers.get('Authentication-Results', '')), 'hop_trace': [], 'originating_ip': None, 'mail_servers': []}
        if received_chain:
            for hop in received_chain:
                if hop['ip']:
                    hop['reverse_dns'] = cls.reverse_dns_lookup(hop['ip'])
                    analysis['hop_trace'].append(hop)
            if analysis['hop_trace']: analysis['originating_ip'] = analysis['hop_trace'][0]['ip']
        
        analysis['auth_risk_score'] = 0
        if analysis['authentication']['spf']['status'].lower() in ['none', 'fail', 'softfail', 'permerror', 'temperror']: analysis['auth_risk_score'] += 35
        if analysis['authentication']['dkim']['status'].lower() in ['none', 'fail', 'permerror', 'temperror']: analysis['auth_risk_score'] += 35
        if analysis['authentication']['dmarc']['status'].lower() in ['none', 'fail', 'quarantine', 'reject', 'permerror', 'temperror']: analysis['auth_risk_score'] += 40
        analysis['auth_risk_score'] = min(100, analysis['auth_risk_score'])
        return analysis

class URLEngine:
    URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]*'
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        return list(set(re.findall(URLEngine.URL_PATTERN, text)))

    @staticmethod
    def expand_url(url: str, timeout: int = 5) -> Dict:
        result = {'original': url, 'final': url, 'redirects': 0, 'redirect_chain': [], 'is_accessible': False, 'status_code': None, 'error': None}
        try:
            response = requests.head(url, allow_redirects=True, timeout=timeout, verify=False)
            result.update({'final': response.url, 'redirects': len(response.history), 'redirect_chain': [r.url for r in response.history], 'status_code': response.status_code, 'is_accessible': response.status_code < 400})
        except requests.Timeout: result['error'] = 'Timeout'
        except requests.RequestException as e: result['error'] = str(e)
        except Exception as e: result['error'] = f"Unexpected error: {e}"
        return result

    @staticmethod
    def check_suspicious_patterns(url: str) -> Dict:
        result = {'url': url, 'suspicious_indicators': [], 'risk_score': 0}
        url_lower = url.lower()
        if any(pattern in url_lower for pattern in ['bit.ly', 'tinyurl', 'short.link']):
            result['suspicious_indicators'].append('Known URL shortener')
            result['risk_score'] += 15
        if '%' in url:
            result['suspicious_indicators'].append('URL encoded characters')
            result['risk_score'] += 10
        if re.search(r'https?://(\d{1,3}\.){3}\d{1,3}', url):
            result['suspicious_indicators'].append('Direct IP address (no domain)')
            result['risk_score'] += 20
        if urlparse(url).netloc.count('.') > 2:
            result['suspicious_indicators'].append('Excessive subdomains')
            result['risk_score'] += 10
        return result

    @classmethod
    def process_single_url(cls, url: str) -> Dict:
        url_analysis = {'url': url, 'expanded': cls.expand_url(url), 'suspicious_check': cls.check_suspicious_patterns(url)}
        url_risk = url_analysis['suspicious_check']['risk_score']
        if url_analysis['expanded']['redirects'] > 3: url_risk += 10
        url_analysis['risk_score'] = url_risk
        return url_analysis

    @classmethod
    def analyze(cls, text: str, html: str = "") -> Dict:
        urls = cls.extract_urls(text + " " + html)
        analysis = {'total_urls': len(urls), 'urls': [], 'overall_risk_score': 0}
        if urls:
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(urls))) as executor:
                results = list(executor.map(cls.process_single_url, urls))
            for res in results:
                analysis['urls'].append(res)
                analysis['overall_risk_score'] += res['risk_score']
            analysis['overall_risk_score'] = min(100, analysis['overall_risk_score'] // len(urls))
        return analysis