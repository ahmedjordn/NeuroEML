# """
# NeuroEML OSINT Enrichment Module
# External threat intelligence integration: VirusTotal, AbuseIPDB
# """

# import requests
# import json
# import logging
# from typing import Dict, List, Optional
# from config.settings import VIRUSTOTAL_API_KEY, ABUSEIPDB_API_KEY, IOC_THRESHOLD_COUNT

# logger = logging.getLogger(__name__)


# class VirusTotalClient:
#     """VirusTotal API integration for hash and URL checking"""

#     BASE_URL = "https://www.virustotal.com/api/v3"

#     def __init__(self, api_key: str = VIRUSTOTAL_API_KEY):
#         self.api_key = api_key
#         self.headers = {
#             "x-apikey": api_key,
#             "User-Agent": "NeuroEML/1.0"
#         }

#     def check_hash(self, file_hash: str) -> Dict:
#         """
#         Check file hash against VirusTotal
        
#         Args:
#             file_hash: MD5, SHA256, or SHA1 hash
            
#         Returns:
#             Analysis results
#         """
        
#         result = {
#             'hash': file_hash,
#             'found': False,
#             'detections': 0,
#             'detection_ratio': '0/0',
#             'vendors': [],
#             'last_analysis_date': None,
#             'error': None
#         }
        
#         if not self.api_key:
#             result['error'] = 'VirusTotal API key not configured'
#             return result
        
#         try:
#             endpoint = f"{self.BASE_URL}/files/{file_hash}"
#             response = requests.get(endpoint, headers=self.headers, timeout=10)
            
#             if response.status_code == 200:
#                 data = response.json()['data']['attributes']
#                 result['found'] = True
                
#                 # Get detection stats
#                 last_analysis = data.get('last_analysis_stats', {})
#                 result['detections'] = last_analysis.get('malicious', 0)
#                 total = sum(last_analysis.values())
#                 result['detection_ratio'] = f"{result['detections']}/{total}"
                
#                 # Get detected vendors
#                 results = data.get('last_analysis_results', {})
#                 for vendor, detection in results.items():
#                     if detection.get('category') == 'malicious':
#                         result['vendors'].append({
#                             'vendor': vendor,
#                             'category': detection.get('category'),
#                             'engine_name': detection.get('engine_name')
#                         })
                
#                 result['last_analysis_date'] = data.get('last_analysis_date')
            
#             elif response.status_code == 404:
#                 result['found'] = False
#             else:
#                 result['error'] = f"API returned status {response.status_code}"
        
#         except requests.exceptions.Timeout:
#             result['error'] = 'VirusTotal API timeout'
#         except Exception as e:
#             result['error'] = str(e)
#             logger.error(f"VirusTotal hash check failed: {e}")
        
#         return result

#     def check_url(self, url: str) -> Dict:
#         """
#         Check URL against VirusTotal
        
#         Args:
#             url: URL to check
            
#         Returns:
#             Analysis results
#         """
        
#         result = {
#             'url': url,
#             'found': False,
#             'detections': 0,
#             'detection_ratio': '0/0',
#             'last_analysis_date': None,
#             'categories': [],
#             'error': None
#         }
        
#         if not self.api_key:
#             result['error'] = 'VirusTotal API key not configured'
#             return result
        
#         try:
#             # URL encode and check
#             endpoint = f"{self.BASE_URL}/urls"
#             payload = {"url": url}
#             response = requests.post(endpoint, headers=self.headers, data=payload, timeout=10)
            
#             if response.status_code == 200:
#                 data = response.json()['data']['attributes']
                
#                 # Get detection stats
#                 last_analysis = data.get('last_analysis_stats', {})
#                 result['detections'] = last_analysis.get('malicious', 0)
#                 total = sum(last_analysis.values())
#                 result['detection_ratio'] = f"{result['detections']}/{total}"
#                 result['found'] = True
                
#                 # Get categories
#                 result['categories'] = data.get('categories', {})
#                 result['last_analysis_date'] = data.get('last_analysis_date')
            
#             else:
#                 result['error'] = f"API returned status {response.status_code}"
        
#         except requests.exceptions.Timeout:
#             result['error'] = 'VirusTotal API timeout'
#         except Exception as e:
#             result['error'] = str(e)
#             logger.error(f"VirusTotal URL check failed: {e}")
        
#         return result


# class AbuseIPDBClient:
#     """AbuseIPDB API integration for IP reputation checking"""

#     BASE_URL = "https://api.abuseipdb.com/api/v2/check"

#     def __init__(self, api_key: str = ABUSEIPDB_API_KEY):
#         self.api_key = api_key

#     def check_ip(self, ip_address: str) -> Dict:
#         """
#         Check IP reputation against AbuseIPDB
        
#         Args:
#             ip_address: IP to check
            
#         Returns:
#             Reputation data
#         """
        
#         result = {
#             'ip': ip_address,
#             'abuse_score': 0,
#             'total_reports': 0,
#             'last_reported_at': None,
#             'usage_type': None,
#             'is_whitelisted': False,
#             'error': None,
#             'categories': []
#         }
        
#         if not self.api_key:
#             result['error'] = 'AbuseIPDB API key not configured'
#             return result
        
#         try:
#             headers = {
#                 'Key': self.api_key,
#                 'Accept': 'application/json'
#             }
            
#             params = {
#                 'ipAddress': ip_address,
#                 'maxAgeInDays': 90,
#                 'verbose': ''
#             }
            
#             response = requests.get(self.BASE_URL, headers=headers, params=params, timeout=10)
            
#             if response.status_code == 200:
#                 data = response.json()['data']
#                 result['abuse_score'] = data.get('abuseConfidenceScore', 0)
#                 result['total_reports'] = data.get('totalReports', 0)
#                 result['last_reported_at'] = data.get('lastReportedAt')
#                 result['usage_type'] = data.get('usageType')
#                 result['is_whitelisted'] = data.get('isWhitelisted', False)
                
#                 # Get report categories
#                 reports = data.get('reports', [])
#                 categories = set()
#                 for report in reports:
#                     categories.update(report.get('categories', []))
#                 result['categories'] = list(categories)
            
#             else:
#                 result['error'] = f"API returned status {response.status_code}"
        
#         except requests.exceptions.Timeout:
#             result['error'] = 'AbuseIPDB API timeout'
#         except Exception as e:
#             result['error'] = str(e)
#             logger.error(f"AbuseIPDB check failed: {e}")
        
#         return result


# class IOCEnricher:
#     """
#     Enriches IOCs (Indicators of Compromise) with external threat intelligence
#     Checks URLs, IPs, domains, and file hashes against public databases
#     """

#     def __init__(self):
#         self.vt_client = VirusTotalClient()
#         self.abuseipdb_client = AbuseIPDBClient()

#     def enrich_iocs(self, 
#                     urls: List[str] = None, 
#                     ips: List[str] = None, 
#                     hashes: List[str] = None) -> Dict:
#         """
#         Enrich all IOCs with threat intelligence
        
#         Args:
#             urls: List of URLs to check
#             ips: List of IPs to check
#             hashes: List of file hashes to check
            
#         Returns:
#             Enriched IOC data with detections
#         """
        
#         enrichment = {
#             'total_iocs': 0,
#             'flagged_iocs': 0,
#             'urls': [],
#             'ips': [],
#             'hashes': [],
#             'high_risk_indicators': [],
#             'osint_risk_score': 0
#         }
        
#         urls = urls or []
#         ips = ips or []
#         hashes = hashes or []
        
#         # Check URLs
#         for url in urls:
#             vt_result = self.vt_client.check_url(url)
#             enrichment['urls'].append(vt_result)
#             enrichment['total_iocs'] += 1
            
#             if vt_result.get('detections', 0) > 0:
#                 enrichment['flagged_iocs'] += 1
#                 enrichment['high_risk_indicators'].append({
#                     'type': 'url',
#                     'value': url,
#                     'detections': vt_result['detections']
#                 })
        
#         # Check IPs
#         for ip in ips:
#             abuseipdb_result = self.abuseipdb_client.check_ip(ip)
#             enrichment['ips'].append(abuseipdb_result)
#             enrichment['total_iocs'] += 1
            
#             if abuseipdb_result.get('abuse_score', 0) > 25:
#                 enrichment['flagged_iocs'] += 1
#                 enrichment['high_risk_indicators'].append({
#                     'type': 'ip',
#                     'value': ip,
#                     'abuse_score': abuseipdb_result['abuse_score']
#                 })
        
#         # Check Hashes
#         for file_hash in hashes:
#             vt_result = self.vt_client.check_hash(file_hash)
#             enrichment['hashes'].append(vt_result)
#             enrichment['total_iocs'] += 1
            
#             if vt_result.get('detections', 0) > 0:
#                 enrichment['flagged_iocs'] += 1
#                 enrichment['high_risk_indicators'].append({
#                     'type': 'hash',
#                     'value': file_hash,
#                     'detections': vt_result['detections']
#                 })
        
#         # Calculate OSINT risk score
#         if enrichment['total_iocs'] > 0:
#             detection_ratio = enrichment['flagged_iocs'] / enrichment['total_iocs']
#             enrichment['osint_risk_score'] = int(detection_ratio * 100)
        
#         return enrichment


# def extract_iocs(parsed_email: Dict, analysis_engines: Dict) -> Dict:
#     """
#     Extract IOCs from parsed email and engine analysis results
    
#     Args:
#         parsed_email: Parsed email data
#         analysis_engines: Results from Identity, Header, URL engines
        
#     Returns:
#         Dictionary of IOCs organized by type
#     """
    
#     iocs = {
#         'urls': [],
#         'ips': [],
#         'domains': [],
#         'hashes': [],
#         'emails': []
#     }
    
#     # Extract URLs from URL engine
#     for url_analysis in analysis_engines.get('url_engine', {}).get('urls', []):
#         iocs['urls'].append(url_analysis['url'])
    
#     # Extract IPs from received chain
#     for hop in parsed_email.get('received_chain', []):
#         if hop.get('ip'):
#             iocs['ips'].append(hop['ip'])
    
#     # Extract from headers
#     from_header = parsed_email.get('headers', {}).get('From', '')
#     if from_header:
#         import re
#         email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+'
#         emails = re.findall(email_pattern, from_header)
#         iocs['emails'].extend(emails)
        
#         # Extract domains from emails
#         for email in emails:
#             domain = email.split('@')[1]
#             if domain not in iocs['domains']:
#                 iocs['domains'].append(domain)
    
#     # Extract file hashes from attachments
#     for attachment in parsed_email.get('attachments', []):
#         if attachment.get('sha256'):
#             iocs['hashes'].append(attachment['sha256'])
#         if attachment.get('md5'):
#             iocs['hashes'].append(attachment['md5'])
    
#     return iocs
"""
NeuroEML OSINT Enrichment Module
External threat intelligence integration: VirusTotal, AbuseIPDB
"""

import requests
import json
import logging
import base64
from typing import Dict, List, Optional
from config.settings import VIRUSTOTAL_API_KEY, ABUSEIPDB_API_KEY, IOC_THRESHOLD_COUNT

logger = logging.getLogger(__name__)


class VirusTotalClient:
    """VirusTotal API integration for hash and URL checking"""

    BASE_URL = "https://www.virustotal.com/api/v3"

    def __init__(self, api_key: str = VIRUSTOTAL_API_KEY):
        self.api_key = api_key
        self.headers = {
            "x-apikey": api_key,
            "User-Agent": "NeuroEML/1.0"
        }

    def check_hash(self, file_hash: str) -> Dict:
        """
        Check file hash against VirusTotal
        """
        result = {
            'hash': file_hash,
            'found': False,
            'detections': 0,
            'detection_ratio': '0/0',
            'vendors': [],
            'last_analysis_date': None,
            'error': None
        }
        
        if not self.api_key:
            result['error'] = 'VirusTotal API key not configured'
            return result
        
        try:
            endpoint = f"{self.BASE_URL}/files/{file_hash}"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                result_json = response.json()
                attributes = result_json.get('data', {}).get('attributes', {})
                
                if not attributes:
                    result['error'] = 'No scan data available'
                    return result

                result['found'] = True
                
                # Get detection stats safely
                last_analysis = attributes.get('last_analysis_stats', {})
                result['detections'] = last_analysis.get('malicious', 0)
                total = sum(last_analysis.values()) if last_analysis else 0
                result['detection_ratio'] = f"{result['detections']}/{total}" if total > 0 else "0/0"
                
                # Get detected vendors safely
                results = attributes.get('last_analysis_results', {})
                for vendor, detection in results.items():
                    if isinstance(detection, dict) and detection.get('category') == 'malicious':
                        result['vendors'].append({
                            'vendor': vendor,
                            'category': detection.get('category'),
                            'engine_name': detection.get('engine_name')
                        })
                
                result['last_analysis_date'] = attributes.get('last_analysis_date')
            
            elif response.status_code == 404:
                result['found'] = False
                result['error'] = 'Hash not found in VirusTotal database'
            elif response.status_code == 429:
                result['error'] = 'VirusTotal API rate limit exceeded'
            else:
                result['error'] = f"API returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            result['error'] = 'VirusTotal API timeout'
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"VirusTotal hash check failed: {e}")
        
        return result

    def check_url(self, url: str) -> Dict:
        """
        Check URL against VirusTotal using GET report endpoint
        """
        result = {
            'url': url,
            'found': False,
            'detections': 0,
            'detection_ratio': '0/0',
            'last_analysis_date': None,
            'categories': [],
            'error': None
        }
        
        if not self.api_key:
            result['error'] = 'VirusTotal API key not configured'
            return result
        
        try:
            # VirusTotal API v3 requires the URL to be base64url encoded without padding "="
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            endpoint = f"{self.BASE_URL}/urls/{url_id}"
            
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                result_json = response.json()
                attributes = result_json.get('data', {}).get('attributes', {})
                
                if not attributes:
                    result['error'] = 'No scan data available (unscanned URL)'
                    return result
                
                # Get detection stats safely
                last_analysis = attributes.get('last_analysis_stats', {})
                result['detections'] = last_analysis.get('malicious', 0)
                total = sum(last_analysis.values()) if last_analysis else 0
                result['detection_ratio'] = f"{result['detections']}/{total}" if total > 0 else "0/0"
                result['found'] = True
                
                # Get categories safely
                result['categories'] = attributes.get('categories', {})
                result['last_analysis_date'] = attributes.get('last_analysis_date')
            
            elif response.status_code == 404:
                result['found'] = False
                result['error'] = 'URL not found in VirusTotal database (Never scanned before)'
            elif response.status_code == 429:
                result['error'] = 'VirusTotal API rate limit exceeded'
            else:
                result['error'] = f"API returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            result['error'] = 'VirusTotal API timeout'
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"VirusTotal URL check failed: {e}")
        
        return result


class AbuseIPDBClient:
    """AbuseIPDB API integration for IP reputation checking"""

    BASE_URL = "https://api.abuseipdb.com/api/v2/check"

    def __init__(self, api_key: str = ABUSEIPDB_API_KEY):
        self.api_key = api_key

    def check_ip(self, ip_address: str) -> Dict:
        """
        Check IP reputation against AbuseIPDB
        """
        result = {
            'ip': ip_address,
            'abuse_score': 0,
            'total_reports': 0,
            'last_reported_at': None,
            'usage_type': None,
            'is_whitelisted': False,
            'error': None,
            'categories': []
        }
        
        if not self.api_key:
            result['error'] = 'AbuseIPDB API key not configured'
            return result
        
        try:
            headers = {
                'Key': self.api_key,
                'Accept': 'application/json'
            }
            params = {
                'ipAddress': ip_address,
                'maxAgeInDays': 90,
                'verbose': ''
            }
            
            response = requests.get(self.BASE_URL, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                result['abuse_score'] = data.get('abuseConfidenceScore', 0)
                result['total_reports'] = data.get('totalReports', 0)
                result['last_reported_at'] = data.get('lastReportedAt')
                result['usage_type'] = data.get('usageType')
                result['is_whitelisted'] = data.get('isWhitelisted', False)
                
                reports = data.get('reports', [])
                categories = set()
                for report in reports:
                    categories.update(report.get('categories', []))
                result['categories'] = list(categories)
            
            elif response.status_code == 429:
                result['error'] = 'AbuseIPDB API rate limit exceeded'
            else:
                result['error'] = f"API returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            result['error'] = 'AbuseIPDB API timeout'
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"AbuseIPDB check failed: {e}")
        
        return result


class IOCEnricher:
    """
    Enriches IOCs (Indicators of Compromise) with external threat intelligence
    Checks URLs, IPs, domains, and file hashes against public databases
    """

    def __init__(self):
        self.vt_client = VirusTotalClient()
        self.abuseipdb_client = AbuseIPDBClient()

    def enrich_iocs(self, 
                    urls: List[str] = None, 
                    ips: List[str] = None, 
                    hashes: List[str] = None) -> Dict:
        """
        Enrich all IOCs with threat intelligence
        """
        enrichment = {
            'total_iocs': 0,
            'flagged_iocs': 0,
            'urls': [],
            'ips': [],
            'hashes': [],
            'high_risk_indicators': [],
            'osint_risk_score': 0
        }
        
        urls = urls or []
        ips = ips or []
        hashes = hashes or []
        
        # Check URLs
        for url in urls:
            vt_result = self.vt_client.check_url(url)
            enrichment['urls'].append(vt_result)
            enrichment['total_iocs'] += 1
            
            if vt_result.get('detections', 0) > 0:
                enrichment['flagged_iocs'] += 1
                enrichment['high_risk_indicators'].append({
                    'type': 'url',
                    'value': url,
                    'detections': vt_result['detections']
                })
        
        # Check IPs
        for ip in ips:
            abuseipdb_result = self.abuseipdb_client.check_ip(ip)
            enrichment['ips'].append(abuseipdb_result)
            enrichment['total_iocs'] += 1
            
            if abuseipdb_result.get('abuse_score', 0) > 25:
                enrichment['flagged_iocs'] += 1
                enrichment['high_risk_indicators'].append({
                    'type': 'ip',
                    'value': ip,
                    'abuse_score': abuseipdb_result['abuse_score']
                })
        
        # Check Hashes
        for file_hash in hashes:
            vt_result = self.vt_client.check_hash(file_hash)
            enrichment['hashes'].append(vt_result)
            enrichment['total_iocs'] += 1
            
            if vt_result.get('detections', 0) > 0:
                enrichment['flagged_iocs'] += 1
                enrichment['high_risk_indicators'].append({
                    'type': 'hash',
                    'value': file_hash,
                    'detections': vt_result['detections']
                })
        
        # Calculate OSINT risk score
        if enrichment['total_iocs'] > 0:
            detection_ratio = enrichment['flagged_iocs'] / enrichment['total_iocs']
            enrichment['osint_risk_score'] = int(detection_ratio * 100)
        
        return enrichment


def extract_iocs(parsed_email: Dict, analysis_engines: Dict) -> Dict:
    """
    Extract IOCs from parsed email and engine analysis results
    """
    iocs = {
        'urls': [],
        'ips': [],
        'domains': [],
        'hashes': [],
        'emails': []
    }
    
    # Extract URLs from URL engine
    for url_analysis in analysis_engines.get('url_engine', {}).get('urls', []):
        iocs['urls'].append(url_analysis['url'])
    
    # Extract IPs from received chain
    for hop in parsed_email.get('received_chain', []):
        if hop.get('ip'):
            iocs['ips'].append(hop['ip'])
    
    # Extract from headers
    from_header = parsed_email.get('headers', {}).get('From', '')
    if from_header:
        import re
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+'
        emails = re.findall(email_pattern, from_header)
        iocs['emails'].extend(emails)
        
        # Extract domains from emails
        for email in emails:
            try:
                domain = email.split('@')[1]
                if domain not in iocs['domains']:
                    iocs['domains'].append(domain)
            except IndexError:
                continue
    
    # Extract file hashes from attachments
    for attachment in parsed_email.get('attachments', []):
        if attachment.get('sha256'):
            iocs['hashes'].append(attachment['sha256'])
        if attachment.get('md5'):
            iocs['hashes'].append(attachment['md5'])
    
    return iocs