"""
NeuroEML Analysis Orchestrator
Main workflow that combines parsing, engines, AI analysis, and OSINT enrichment
"""

import logging
import json
import concurrent.futures
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from parsers.email_parser import EmailParser
from engines.analysis_engines import IdentityEngine, HeaderEngine, URLEngine
from engines.ai_analysis import DualPassAnalysis
from engines.osint_enrichment import IOCEnricher, extract_iocs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NeuroEMLAnalyzer:
    def __init__(self):
        self.parser = EmailParser()
        self.dual_pass = DualPassAnalysis()
        self.osint = IOCEnricher()

    def analyze_email(self, eml_file_path: str) -> Dict:
        logger.info(f"Starting NeuroEML analysis for: {eml_file_path}")
        
        report = {
            'metadata': {
                'analysis_timestamp': datetime.now().isoformat(),
                'file_path': eml_file_path,
                'status': 'running'
            },
            'parsing': {},
            'engines': {},
            'ai_analysis': {},
            'osint_enrichment': {},
            'final_risk_score': 0,
            'risk_level': 'unknown',
            'recommendations': []
        }
        
        try:
            # Step 1: Parse Email
            logger.info("Step 1: Parsing email file...")
            parsed_email = self.parser.parse_file(eml_file_path)
            report['parsing'] = {
                'success': True,
                'headers_count': len(parsed_email.get('headers', {})),
                'attachments_count': len(parsed_email.get('attachments', [])),
                'has_html_body': bool(parsed_email['body'].get('html')),
                'has_text_body': bool(parsed_email['body'].get('text'))
            }
            
            # Step 2: Run Analysis Engines (Parallel)
            logger.info("Step 2: Running analysis engines...")
            report['engines'] = self._run_engines(parsed_email)
            
            # Step 3: AI Dual-Pass Analysis
            logger.info("Step 3: Running AI analysis passes...")
            ai_result = self.dual_pass.analyze(
                parsed_email['body'].get('text', ''),
                parsed_email['body'].get('html', '')
            )
            report['ai_analysis'] = ai_result.get('ai_analysis', ai_result)
            
            # Step 4: Extract IOCs and OSINT Enrichment
            logger.info("Step 4: Extracting IOCs and enriching with OSINT...")
            iocs = extract_iocs(parsed_email, report['engines'])
            report['osint_enrichment'] = self.osint.enrich_iocs(
                urls=iocs.get('urls'),
                ips=iocs.get('ips'),
                hashes=iocs.get('hashes')
            )
            
            # Step 5: Calculate Final Risk Score
            logger.info("Step 5: Calculating final risk score...")
            report['final_risk_score'] = self._calculate_risk_score(report)
            report['risk_level'] = self._determine_risk_level(report['final_risk_score'])
            
            # Generate Recommendations
            report['recommendations'] = self._generate_recommendations(report)
            
            report['metadata']['status'] = 'completed'
            logger.info(f"Analysis completed. Risk Score: {report['final_risk_score']}, Level: {report['risk_level']}")
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            report['metadata']['status'] = 'failed'
            report['metadata']['error'] = str(e)
        
        return report

    def _run_engines(self, parsed_email: Dict) -> Dict:
        """Run Identity, Header, and URL engines in PARALLEL threads"""
        engines_report = {'identity_engine': {}, 'header_engine': {}, 'url_engine': {}}
        
        from_header = parsed_email.get('headers', {}).get('From', '')
        headers = parsed_email.get('headers', {})
        received_chain = parsed_email.get('received_chain', [])
        text_body = parsed_email.get('body', {}).get('text', '')
        html_body = parsed_email.get('body', {}).get('html', '')

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_identity = executor.submit(IdentityEngine.analyze, from_header) if from_header else None
                future_header = executor.submit(HeaderEngine.analyze, headers, received_chain)
                future_url = executor.submit(URLEngine.analyze, text_body, html_body)

                if future_identity:
                    engines_report['identity_engine'] = future_identity.result()
                engines_report['header_engine'] = future_header.result()
                engines_report['url_engine'] = future_url.result()
        except Exception as e:
            logger.error(f"Parallel engine execution failed: {e}")
        
        return engines_report

    @staticmethod
    def _calculate_risk_score(report: Dict) -> int:
        scores = {
            'identity': report.get('engines', {}).get('identity_engine', {}).get('risk_score', 0),
            'header': report.get('engines', {}).get('header_engine', {}).get('auth_risk_score', 0),
            'url': report.get('engines', {}).get('url_engine', {}).get('overall_risk_score', 0),
            'profiler': report.get('ai_analysis', {}).get('profiler', {}).get('overall_suspicion_score', 0),
            'auditor': report.get('ai_analysis', {}).get('auditor', {}).get('technical_risk_score', 0),
            'osint': report.get('osint_enrichment', {}).get('osint_risk_score', 0)
        }
        
        auth_results = report.get('engines', {}).get('header_engine', {}).get('authentication', {})
        spf_failed = auth_results.get('spf', {}).get('status', '').lower() not in ['pass']
        dkim_failed = auth_results.get('dkim', {}).get('status', '').lower() not in ['pass']
        dmarc_failed = auth_results.get('dmarc', {}).get('status', '').lower() not in ['pass']
        
        auth_fail_count = sum([spf_failed, dkim_failed, dmarc_failed])
        if spf_failed or dkim_failed or dmarc_failed: scores['header'] = max(scores['header'], 50)
        if auth_fail_count == 3: scores['header'] = 100 
        elif auth_fail_count == 2: scores['header'] = max(scores['header'], 85)
        
        identity = report.get('engines', {}).get('identity_engine', {})
        is_spoofing = identity.get('homograph_check', {}).get('is_spoofing_attempt', False)
        is_punycode = identity.get('punycode_check', {}).get('is_suspicious', False)
        
        if is_spoofing: scores['identity'] = max(scores['identity'], 90)
        elif is_punycode: scores['identity'] = max(scores['identity'], 85)
        
        final_score = int(
            (scores['header'] * 0.40) + (scores['identity'] * 0.25) +
            (scores['url'] * 0.15) + (scores['profiler'] * 0.10) + 
            (scores['auditor'] * 0.08) + (scores['osint'] * 0.02)
        )
        
        if auth_fail_count == 3: final_score = max(final_score, 65)
        if is_spoofing or is_punycode: final_score = max(final_score, 50)
            
        return min(100, max(0, final_score))

    @staticmethod
    def _determine_risk_level(score: int) -> str:
        if score >= 80: return "CRITICAL"
        elif score >= 60: return "HIGH"
        elif score >= 40: return "MEDIUM"
        elif score >= 20: return "LOW"
        else: return "SAFE"

    @staticmethod
    def _generate_recommendations(report: Dict) -> list:
        recommendations = []
        risk_score = report.get('final_risk_score', 0)
        
        header_engine = report.get('engines', {}).get('header_engine', {})
        auth = header_engine.get('authentication', {})
        auth_fail_count = 0
        
        if auth.get('spf', {}).get('status') in ['none', 'fail', 'softfail']: auth_fail_count += 1
        if auth.get('dkim', {}).get('status') in ['none', 'fail']: auth_fail_count += 1
        if auth.get('dmarc', {}).get('status') in ['none', 'fail']: auth_fail_count += 1
        
        identity_engine = report.get('engines', {}).get('identity_engine', {})
        is_spoofing = identity_engine.get('homograph_check', {}).get('is_spoofing_attempt')
        is_punycode = identity_engine.get('punycode_check', {}).get('is_suspicious')
        
        if auth_fail_count >= 3 or is_spoofing or is_punycode:
            recommendations.extend(["🚨 CRITICAL: ALL authentication methods FAILED - Email is likely SPOOFED", "🚨 Block sender immediately. Do NOT trust this email.", "🚨 Report to security team as potential phishing/spoofing attack."])
        elif risk_score >= 80:
            recommendations.extend(["🚨 CRITICAL: Block sender immediately. Mark as malicious.", "🚨 Do not click any links or open attachments.", "🚨 Report to security team for incident response."])
        elif risk_score >= 60:
            recommendations.extend(["⚠️ HIGH RISK: Likely malicious email. Verify sender through alternative channel.", "⚠️ Do not download or execute attachments without validation.", "⚠️ Consider sandboxing any suspicious files."])
        elif risk_score >= 40:
            recommendations.extend(["⚡ MEDIUM RISK: Review carefully. Verify unexpected requests directly with sender.", "⚡ Be suspicious of urgent language or threats."])
        
        if is_punycode: recommendations.append("🔴 CRITICAL: Punycode domain detected - homograph attack (look-alike domain)")
        if is_spoofing: recommendations.append("🔴 CRITICAL: Display name spoofing detected - sender IMPERSONATION ATTEMPT")
        if auth.get('spf', {}).get('status') in ['none', 'fail', 'softfail']: recommendations.append("📧 SPF FAILED - Email FAILED sender authentication - likely SPOOFED")
        if auth.get('dkim', {}).get('status') in ['none', 'fail']: recommendations.append("📧 DKIM FAILED - Email may be TAMPERED or FORGED")
        if auth.get('dmarc', {}).get('status') in ['none', 'fail']: recommendations.append("📧 DMARC FAILED - Domain policy VIOLATED")
        
        high_risk_iocs = report.get('osint_enrichment', {}).get('high_risk_indicators', [])
        if high_risk_iocs: recommendations.append(f"🔗 CRITICAL: Found {len(high_risk_iocs)} flagged IOCs - Detected by threat intelligence as MALICIOUS")
        
        auditor_findings = report.get('ai_analysis', {}).get('auditor', {}).get('critical_findings', [])
        if auditor_findings: recommendations.append(f"🔒 ALERT: Technical analysis detected malicious patterns: {', '.join(auditor_findings[:2])}")
        
        profiler_findings = report.get('ai_analysis', {}).get('profiler', {}).get('tactics', {})
        if profiler_findings:
            high_score_tactics = [k for k, v in profiler_findings.items() if isinstance(v, dict) and v.get('score', 0) >= 7]
            if high_score_tactics: recommendations.append(f"⚠️ ALERT: Strong social engineering tactics detected: {', '.join(high_score_tactics)}")
        
        url_engine = report.get('engines', {}).get('url_engine', {})
        if url_engine.get('overall_risk_score', 0) >= 50: recommendations.append("🔗 WARNING: Email contains suspicious/malicious URLs")
        
        return recommendations