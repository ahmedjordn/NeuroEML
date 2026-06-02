# """
# NeuroEML AI Analysis Module
# Dual-pass AI analysis: Profiler (psychological triggers) and Auditor (technical obfuscation)
# Uses Ollama for local model inference
# """

# import requests
# import json
# import logging
# from typing import Dict, List, Optional
# from config.settings import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT

# logger = logging.getLogger(__name__)


# class OllamaClient:
#     """Interface to Ollama local LLM"""

#     def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
#         self.host = host
#         self.model = model
#         self.api_endpoint = f"{host}/api/generate"

#     def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 500) -> Optional[str]:
#         """
#         Generate response from Ollama model
        
#         Args:
#             prompt: The input prompt
#             temperature: Sampling temperature (0.0 = deterministic, 1.0 = random)
#             max_tokens: Maximum tokens to generate
            
#         Returns:
#             Generated text or None on error
#         """
#         payload = {
#             "model": self.model,
#             "prompt": prompt,
#             "temperature": temperature,
#             "num_predict": max_tokens,
#             "stream": False
#         }
        
#         try:
#             response = requests.post(
#                 self.api_endpoint,
#                 json=payload,
#                 timeout=OLLAMA_TIMEOUT
#             )
#             response.raise_for_status()
            
#             result = response.json()
#             return result.get('response', '').strip()
        
#         except requests.exceptions.ConnectionError:
#             logger.error(f"Failed to connect to Ollama at {self.host}")
#             return None
#         except requests.exceptions.Timeout:
#             logger.error(f"Ollama request timed out after {OLLAMA_TIMEOUT}s")
#             return None
#         except Exception as e:
#             logger.error(f"Ollama API error: {e}")
#             return None

#     def is_available(self) -> bool:
#         """Check if Ollama is running and accessible"""
#         try:
#             response = requests.get(f"{self.host}/api/tags", timeout=5)
#             return response.status_code == 200
#         except Exception:
#             return False


# class AIProfiler:
#     """
#     Pass A: Psychological Analysis
#     Analyzes email text body for social engineering tactics:
#     - Urgency/Time pressure
#     - Authority/Impersonation
#     - Fear/Threat appeals
#     - Obligation/Duty
#     - Social proof
#     - Scarcity
#     """

#     PROFILER_PROMPT_TEMPLATE = """Analyze this email text for social engineering tactics and psychological triggers.

# Email Body:
# ---
# {email_text}
# ---

# Identify and rate the following tactics on a scale of 0-10:
# 1. Urgency/Time Pressure (words like "immediate", "urgent", "act now")
# 2. Authority/Trust Exploitation (claims of official positions, logos)
# 3. Fear Appeal (threats, warnings, account problems)
# 4. Obligation/Duty (personal responsibility pressure)
# 5. Social Proof (bandwagon, "others have done this")
# 6. Scarcity (limited offers, exclusive deals)
# 7. Authority/Impersonation (False authority claims)

# Format your response as JSON:
# {{
#   "tactics": {{
#     "urgency": {{"score": 0-10, "indicators": ["list of specific phrases"]}},
#     "authority": {{"score": 0-10, "indicators": []}},
#     "fear": {{"score": 0-10, "indicators": []}},
#     "obligation": {{"score": 0-10, "indicators": []}},
#     "social_proof": {{"score": 0-10, "indicators": []}},
#     "scarcity": {{"score": 0-10, "indicators": []}},
#     "impersonation": {{"score": 0-10, "indicators": []}}
#   }},
#   "overall_suspicion_score": 0-100,
#   "summary": "Brief analysis of the social engineering tactics detected"
# }}

# Be concise and focus on actual evidence from the email text."""

#     def __init__(self, ollama_client: OllamaClient):
#         self.client = ollama_client

#     def analyze(self, email_text: str) -> Dict:
#         """Analyze email for social engineering tactics"""
        
#         result = {
#             'pass_name': 'Profiler (Psychological Analysis)',
#             'email_preview': email_text[:200] + "..." if len(email_text) > 200 else email_text,
#             'tactics': {},
#             'overall_suspicion_score': 0,
#             'summary': '',
#             'error': None,
#             'raw_response': ''
#         }
        
#         if not email_text or len(email_text.strip()) < 10:
#             result['error'] = 'Email text too short for analysis'
#             return result
        
#         prompt = self.PROFILER_PROMPT_TEMPLATE.format(email_text=email_text[:2000])
        
#         logger.info("Running Profiler analysis...")
#         response = self.client.generate(prompt, temperature=0.3, max_tokens=800)
        
#         if not response:
#             result['error'] = 'Failed to get response from Ollama'
#             return result
        
#         result['raw_response'] = response
        
#         # Try to parse JSON response
#         try:
#             # Find JSON in response
#             import re
#             json_match = re.search(r'\{.*\}', response, re.DOTALL)
#             if json_match:
#                 parsed = json.loads(json_match.group())
#                 result['tactics'] = parsed.get('tactics', {})
#                 result['overall_suspicion_score'] = parsed.get('overall_suspicion_score', 0)
#                 result['summary'] = parsed.get('summary', '')
#             else:
#                 logger.warning("Could not find JSON in Profiler response")
#                 result['summary'] = response
#         except json.JSONDecodeError as e:
#             logger.warning(f"Failed to parse Profiler JSON: {e}")
#             result['summary'] = response
        
#         return result


# class AIAuditor:
#     """
#     Pass B: Technical Analysis
#     Analyzes HTML body for technical obfuscation and malicious patterns:
#     - Base64 encoded scripts
#     - Obfuscated JavaScript
#     - Hidden div/iframe elements
#     - Suspicious form actions
#     - Tracking pixels
#     - Form exfiltration
#     """

#     AUDITOR_PROMPT_TEMPLATE = """Analyze this email HTML for technical malicious patterns and obfuscation.

# Email HTML:
# ---
# {email_html}
# ---

# Check for these technical threats:
# 1. Hidden elements (display:none, visibility:hidden divs, iframes)
# 2. Form elements (especially hidden forms targeting external URLs)
# 3. JavaScript obfuscation (unescape(), eval(), atob())
# 4. Base64 encoded content
# 5. Tracking pixels and external resources
# 6. Credential harvesting patterns
# 7. Exploit kit indicators
# 8. Suspicious <iframe> tags

# Format your response as JSON:
# {{
#   "threats": {{
#     "hidden_elements": {{"found": true/false, "count": 0, "details": []}},
#     "form_elements": {{"found": true/false, "count": 0, "details": ["target URLs"]}},
#     "script_obfuscation": {{"found": true/false, "details": []}},
#     "base64_content": {{"found": true/false, "details": []}},
#     "tracking": {{"found": true/false, "count": 0, "details": []}},
#     "credential_harvest": {{"found": true/false, "details": []}},
#     "exploit_indicators": {{"found": true/false, "details": []}},
#     "suspicious_iframes": {{"found": true/false, "count": 0, "details": []}}
#   }},
#   "technical_risk_score": 0-100,
#   "critical_findings": ["list of critical issues"],
#   "recommendations": "Security recommendations"
# }}

# Be technical and precise. Focus on actual malicious patterns, not styling."""

#     def __init__(self, ollama_client: OllamaClient):
#         self.client = ollama_client

#     def analyze(self, email_html: str) -> Dict:
#         """Analyze email HTML for technical threats"""
        
#         result = {
#             'pass_name': 'Auditor (Technical Analysis)',
#             'html_preview': email_html[:200] + "..." if len(email_html) > 200 else email_html,
#             'threats': {},
#             'technical_risk_score': 0,
#             'critical_findings': [],
#             'recommendations': '',
#             'error': None,
#             'raw_response': ''
#         }
        
#         if not email_html or len(email_html.strip()) < 10:
#             result['error'] = 'Email HTML too short for analysis'
#             return result
        
#         prompt = self.AUDITOR_PROMPT_TEMPLATE.format(email_html=email_html[:3000])
        
#         logger.info("Running Auditor analysis...")
#         response = self.client.generate(prompt, temperature=0.3, max_tokens=1000)
        
#         if not response:
#             result['error'] = 'Failed to get response from Ollama'
#             return result
        
#         result['raw_response'] = response
        
#         # Try to parse JSON response
#         try:
#             import re
#             json_match = re.search(r'\{.*\}', response, re.DOTALL)
#             if json_match:
#                 parsed = json.loads(json_match.group())
#                 result['threats'] = parsed.get('threats', {})
#                 result['technical_risk_score'] = parsed.get('technical_risk_score', 0)
#                 result['critical_findings'] = parsed.get('critical_findings', [])
#                 result['recommendations'] = parsed.get('recommendations', '')
#             else:
#                 logger.warning("Could not find JSON in Auditor response")
#                 result['recommendations'] = response
#         except json.JSONDecodeError as e:
#             logger.warning(f"Failed to parse Auditor JSON: {e}")
#             result['recommendations'] = response
        
#         return result


# class DualPassAnalysis:
#     """Orchestrates both Profiler and Auditor passes"""

#     def __init__(self):
#         self.client = OllamaClient()
#         self.profiler = AIProfiler(self.client)
#         self.auditor = AIAuditor(self.client)

#     def is_ready(self) -> bool:
#         """Check if Ollama is available"""
#         return self.client.is_available()

#     def analyze(self, email_text: str, email_html: str = "") -> Dict:
#         """
#         Run both profiler and auditor passes
        
#         Args:
#             email_text: Plain text body
#             email_html: HTML body
            
#         Returns:
#             Combined analysis results
#         """
        
#         analysis = {
#             'ai_analysis': {
#                 'profiler': self.profiler.analyze(email_text),
#                 'auditor': self.auditor.analyze(email_html),
#                 'combined_risk_score': 0
#             },
#             'ollama_status': {
#                 'available': self.client.is_available(),
#                 'model': self.client.model,
#                 'host': self.client.host
#             }
#         }
        
#         # Calculate combined risk score
#         profiler_score = analysis['ai_analysis']['profiler'].get('overall_suspicion_score', 0)
#         auditor_score = analysis['ai_analysis']['auditor'].get('technical_risk_score', 0)
        
#         # Weight: psychological (30%) + technical (70%)
#         analysis['ai_analysis']['combined_risk_score'] = int(
#             (profiler_score * 0.3) + (auditor_score * 0.7)
#         )
        
#         return analysis


# import requests
# import json
# import logging
# import re
# from typing import Dict, List, Optional
# from config.settings import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT

# logger = logging.getLogger(__name__)

# class OllamaClient:
#     def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
#         # Ensure host doesn't have trailing slash for consistency
#         self.host = host.rstrip('/')
#         self.model = model
#         self.api_endpoint = f"{self.host}/api/generate"

#     def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 800) -> Optional[str]:
#         payload = {
#             "model": self.model,
#             "prompt": prompt,
#             "temperature": temperature, # Lowered for more consistent JSON
#             "num_predict": max_tokens,
#             "stream": False,
#             "format": "json" # CRITICAL: Forces Ollama to attempt JSON mode
#         }
        
#         try:
#             response = requests.post(
#                 self.api_endpoint,
#                 json=payload,
#                 timeout=OLLAMA_TIMEOUT
#             )
#             response.raise_for_status()
#             result = response.json()
#             return result.get('response', '').strip()
#         except Exception as e:
#             logger.error(f"Ollama API error: {e}")
#             return None

#     def is_available(self) -> bool:
#         try:
#             response = requests.get(f"{self.host}/api/tags", timeout=5)
#             return response.status_code == 200
#         except Exception:
#             return False

# class AIProfiler:
#     # Added "STRICT JSON" instructions to the template
#     PROFILER_PROMPT_TEMPLATE = """Return ONLY a valid JSON object analyzing this email. No conversational text.
# Email Body:
# ---
# {email_text}
# ---
# Format:
# {{
#   "tactics": {{
#     "urgency": {{"score": 0, "indicators": []}},
#     "authority": {{"score": 0, "indicators": []}},
#     "fear": {{"score": 0, "indicators": []}},
#     "obligation": {{"score": 0, "indicators": []}},
#     "social_proof": {{"score": 0, "indicators": []}},
#     "scarcity": {{"score": 0, "indicators": []}},
#     "impersonation": {{"score": 0, "indicators": []}}
#   }},
#   "overall_suspicion_score": 0,
#   "summary": "Analysis here"
# }}"""

#     def __init__(self, ollama_client: OllamaClient):
#         self.client = ollama_client

#     def _clean_json(self, text: str) -> str:
#         """Removes markdown code blocks and extracts the raw JSON string"""
#         # Remove markdown blocks like ```json ... ```
#         text = re.sub(r'```json\s*|\s*```', '', text)
#         # Find the first { and last }
#         start = text.find('{')
#         end = text.rfind('}')
#         if start != -1 and end != -1:
#             return text[start:end+1]
#         return text

#     def analyze(self, email_text: str) -> Dict:
#         result = {'pass_name': 'Profiler', 'overall_suspicion_score': 0, 'summary': '', 'tactics': {}}
#         prompt = self.PROFILER_PROMPT_TEMPLATE.format(email_text=email_text[:2000])
        
#         response = self.client.generate(prompt)
#         if not response: return result

#         try:
#             cleaned = self._clean_json(response)
#             parsed = json.loads(cleaned)
#             result.update(parsed)
#         except json.JSONDecodeError as e:
#             logger.warning(f"JSON Parse Failed: {e}")
#             result['summary'] = "AI response format was invalid."
#         return result

# class AIAuditor:
#     AUDITOR_PROMPT_TEMPLATE = """Return ONLY a valid JSON object. No intro/outro.
# Email HTML:
# ---
# {email_html}
# ---
# Format:
# {{
#   "threats": {{
#     "hidden_elements": {{"found": false, "details": []}},
#     "form_elements": {{"found": false, "details": []}},
#     "script_obfuscation": {{"found": false, "details": []}},
#     "base64_content": {{"found": false, "details": []}},
#     "tracking": {{"found": false, "details": []}},
#     "credential_harvest": {{"found": false, "details": []}}
#   }},
#   "technical_risk_score": 0,
#   "critical_findings": [],
#   "recommendations": ""
# }}"""

#     def __init__(self, ollama_client: OllamaClient):
#         self.client = ollama_client

#     def analyze(self, email_html: str) -> Dict:
#         result = {'pass_name': 'Auditor', 'technical_risk_score': 0, 'threats': {}}
#         prompt = self.AUDITOR_PROMPT_TEMPLATE.format(email_html=email_html[:3000])
        
#         response = self.client.generate(prompt)
#         if not response: return result

#         try:
#             # Reusing the same cleaning logic is safer
#             cleaned = re.sub(r'```json\s*|\s*```', '', response)
#             start, end = cleaned.find('{'), cleaned.rfind('}')
#             parsed = json.loads(cleaned[start:end+1])
#             result.update(parsed)
#         except Exception:
#             result['recommendations'] = "Technical analysis failed to parse."
#         return result

# class DualPassAnalysis:
#     def __init__(self):
#         self.client = OllamaClient()
#         self.profiler = AIProfiler(self.client)
#         self.auditor = AIAuditor(self.client)

#     def analyze(self, email_text: str, email_html: str = "") -> Dict:
#         p_res = self.profiler.analyze(email_text)
#         a_res = self.auditor.analyze(email_html)
        
#         # Pull scores specifically from the parsed keys
#         p_score = p_res.get('overall_suspicion_score', 0)
#         a_score = a_res.get('technical_risk_score', 0)
        
#         combined = int((p_score * 0.3) + (a_score * 0.7))
        
#         return {
#             'ai_analysis': {
#                 'profiler': p_res,
#                 'auditor': a_res,
#                 'combined_risk_score': combined
#             }
#         }


"""
NeuroEML AI Analysis Module
Dual-pass AI analysis: Profiler (psychological triggers) and Auditor (technical obfuscation)
Uses Ollama for local model inference
"""

import requests
import json
import logging
import re
import concurrent.futures
from typing import Dict, List, Optional
from config.settings import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
        self.host = host.rstrip('/')
        self.model = model
        self.api_endpoint = f"{self.host}/api/generate"

    def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 800) -> Optional[str]:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature, 
            "num_predict": max_tokens,
            "stream": False,
            "format": "json" # CRITICAL: Forces Ollama to attempt JSON mode
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=OLLAMA_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            return result.get('response', '').strip()
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return None

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

class AIProfiler:
    PROFILER_PROMPT_TEMPLATE = """Return ONLY a valid JSON object analyzing this email. No conversational text.
Email Body:
---
{email_text}
---
Format:
{{
  "tactics": {{
    "urgency": {{"score": 0, "indicators": []}},
    "authority": {{"score": 0, "indicators": []}},
    "fear": {{"score": 0, "indicators": []}},
    "obligation": {{"score": 0, "indicators": []}},
    "social_proof": {{"score": 0, "indicators": []}},
    "scarcity": {{"score": 0, "indicators": []}},
    "impersonation": {{"score": 0, "indicators": []}}
  }},
  "overall_suspicion_score": 0,
  "summary": "Analysis here"
}}"""

    def __init__(self, ollama_client: OllamaClient):
        self.client = ollama_client

    def _clean_json(self, text: str) -> str:
        text = re.sub(r'```json\s*|\s*```', '', text)
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            return text[start:end+1]
        return text

    def analyze(self, email_text: str) -> Dict:
        result = {'pass_name': 'Profiler', 'overall_suspicion_score': 0, 'summary': '', 'tactics': {}}
        prompt = self.PROFILER_PROMPT_TEMPLATE.format(email_text=email_text[:2000])
        
        response = self.client.generate(prompt)
        if not response: return result

        try:
            cleaned = self._clean_json(response)
            parsed = json.loads(cleaned)
            result.update(parsed)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON Parse Failed: {e}")
            result['summary'] = "AI response format was invalid."
        return result

class AIAuditor:
    AUDITOR_PROMPT_TEMPLATE = """Return ONLY a valid JSON object. No intro/outro.
Email HTML:
---
{email_html}
---
Format:
{{
  "threats": {{
    "hidden_elements": {{"found": false, "details": []}},
    "form_elements": {{"found": false, "details": []}},
    "script_obfuscation": {{"found": false, "details": []}},
    "base64_content": {{"found": false, "details": []}},
    "tracking": {{"found": false, "details": []}},
    "credential_harvest": {{"found": false, "details": []}}
  }},
  "technical_risk_score": 0,
  "critical_findings": [],
  "recommendations": ""
}}"""

    def __init__(self, ollama_client: OllamaClient):
        self.client = ollama_client

    def analyze(self, email_html: str) -> Dict:
        result = {'pass_name': 'Auditor', 'technical_risk_score': 0, 'threats': {}}
        prompt = self.AUDITOR_PROMPT_TEMPLATE.format(email_html=email_html[:3000])
        
        response = self.client.generate(prompt)
        if not response: return result

        try:
            cleaned = re.sub(r'```json\s*|\s*```', '', response)
            start, end = cleaned.find('{'), cleaned.rfind('}')
            parsed = json.loads(cleaned[start:end+1])
            result.update(parsed)
        except Exception:
            result['recommendations'] = "Technical analysis failed to parse."
        return result

class DualPassAnalysis:
    def __init__(self):
        self.client = OllamaClient()
        self.profiler = AIProfiler(self.client)
        self.auditor = AIAuditor(self.client)

    def is_ready(self) -> bool:
        return self.client.is_available()

    def analyze(self, email_text: str, email_html: str = "") -> Dict:
        """Runs Profiler and Auditor passes SEQUENTIALLY to prevent Ollama 500 crashes"""
        
        logger.info("Running Profiler pass...")
        p_res = self.profiler.analyze(email_text)
        
        logger.info("Running Auditor pass...")
        a_res = self.auditor.analyze(email_html)
        
        # Pull scores specifically from the parsed keys
        p_score = p_res.get('overall_suspicion_score', 0)
        a_score = a_res.get('technical_risk_score', 0)
        
        combined = int((p_score * 0.3) + (a_score * 0.7))
        
        return {
            'ai_analysis': {
                'profiler': p_res,
                'auditor': a_res,
                'combined_risk_score': combined
            }
        }