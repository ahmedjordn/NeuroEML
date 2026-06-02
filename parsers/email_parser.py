"""
NeuroEML Parser Module
Ingestion & Parsing Layer: Converts raw .eml files into structured JSON objects
"""

import email
import json
import re
import hashlib
from pathlib import Path
from email.header import decode_header
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class EmailParser:
    """
    Parses .eml files and extracts structured data into four distinct streams:
    1. Headers (routing info, auth results)
    2. Body (Text) - Human readable message
    3. Body (HTML) - Raw code and scripts
    4. Attachments - Files to analyze
    """

    def __init__(self):
        self.parsed_data = {}

    @staticmethod
    def decode_header_value(header_value):
        """Safely decode email header values"""
        if not header_value:
            return ""
        try:
            decoded_parts = decode_header(header_value)
            result = ""
            for part, charset in decoded_parts:
                if isinstance(part, bytes):
                    result += part.decode(charset or 'utf-8', errors='ignore')
                else:
                    result += str(part)
            return result
        except Exception as e:
            logger.warning(f"Failed to decode header: {e}")
            return str(header_value)

    def extract_headers(self, msg: email.message.Message) -> Dict:
        """Extract and parse email headers"""
        headers = {}
        
        # Critical headers
        critical_headers = [
            'From', 'To', 'Subject', 'Date', 'Message-ID',
            'Received', 'Authentication-Results', 'SPF', 'DKIM', 'DMARC',
            'Return-Path', 'Reply-To', 'Content-Type', 'Sender'
        ]
        
        for header in critical_headers:
            value = msg.get(header)
            if value:
                headers[header] = self.decode_header_value(value)
        
        # Extract all headers for deep inspection
        headers['_all_headers'] = dict(msg.items())
        
        return headers

    def extract_received_chain(self, msg: email.message.Message) -> List[Dict]:
        """Extract IP trace from Received headers"""
        received_chain = []
        received_headers = msg.get_all('Received')
        
        if not received_headers:
            return received_chain
        
        ip_pattern = r'\[([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\]'
        
        for idx, received in enumerate(received_headers):
            hop = {
                'hop_number': idx + 1,
                'raw': received,
                'ip': None,
                'hostname': None,
                'timestamp': None
            }
            
            # Extract IP
            ip_match = re.search(ip_pattern, received)
            if ip_match:
                hop['ip'] = ip_match.group(1)
            
            # Extract hostname
            if 'from' in received.lower():
                hostname_match = re.search(r'from\s+([a-zA-Z0-9.-]+)\s', received, re.IGNORECASE)
                if hostname_match:
                    hop['hostname'] = hostname_match.group(1)
            
            received_chain.append(hop)
        
        return received_chain

    def extract_text_body(self, msg: email.message.Message) -> str:
        """Extract plain text body"""
        text_body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        text_body = part.get_payload(decode=True).decode(
                            part.get_content_charset() or 'utf-8',
                            errors='ignore'
                        )
                    except Exception as e:
                        logger.warning(f"Failed to decode text body: {e}")
        else:
            try:
                text_body = msg.get_payload(decode=True).decode(
                    msg.get_content_charset() or 'utf-8',
                    errors='ignore'
                )
            except Exception as e:
                logger.warning(f"Failed to decode message body: {e}")
        
        return text_body

    def extract_html_body(self, msg: email.message.Message) -> str:
        """Extract HTML body"""
        html_body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    try:
                        html_body = part.get_payload(decode=True).decode(
                            part.get_content_charset() or 'utf-8',
                            errors='ignore'
                        )
                    except Exception as e:
                        logger.warning(f"Failed to decode HTML body: {e}")
        
        return html_body

    def extract_attachments(self, msg: email.message.Message) -> List[Dict]:
        """Extract attachment metadata"""
        attachments = []
        
        if not msg.is_multipart():
            return attachments
        
        # Use iter_attachments() if available (Python 3.11+), otherwise use walk()
        try:
            # Try newer method first (Python 3.11+)
            attachment_parts = msg.iter_attachments()
        except AttributeError:
            # Fallback for older Python versions
            attachment_parts = [part for part in msg.walk() 
                               if part.get_content_disposition() == 'attachment']
        
        for part in attachment_parts:
            filename = part.get_filename()
            if not filename:
                continue
            
            try:
                payload = part.get_payload(decode=True)
                attachment_info = {
                    'filename': filename,
                    'content_type': part.get_content_type(),
                    'size': len(payload),
                    'md5': hashlib.md5(payload).hexdigest(),
                    'sha256': hashlib.sha256(payload).hexdigest(),
                    'is_suspicious': self._check_suspicious_extension(filename)
                }
                attachments.append(attachment_info)
            except Exception as e:
                logger.warning(f"Failed to process attachment {filename}: {e}")
        
        return attachments

    @staticmethod
    def _check_suspicious_extension(filename: str) -> bool:
        """Check if file extension is commonly used in phishing"""
        suspicious_extensions = [
            '.exe', '.bat', '.cmd', '.scr', '.vbs', '.js', '.jar',
            '.zip', '.rar', '.7z', '.iso',
            '.doc', '.docm', '.xls', '.xlsm', '.ppt', '.pptm',
            '.pdf', '.ps1', '.msi'
        ]
        
        file_ext = Path(filename).suffix.lower()
        return file_ext in suspicious_extensions

    def parse_file(self, file_path: str) -> Dict:
        """
        Main parsing function - converts .eml to structured JSON
        
        Args:
            file_path: Path to .eml file
            
        Returns:
            Dictionary with parsed email data
        """
        try:
            with open(file_path, 'rb') as f:
                msg = email.message_from_binary_file(f)
            
            parsed_email = {
                'metadata': {
                    'file_path': str(file_path),
                    'file_size': Path(file_path).stat().st_size,
                    'parser_version': '1.0',
                    'parse_timestamp': str(email.utils.formatdate(localtime=True))
                },
                'headers': self.extract_headers(msg),
                'received_chain': self.extract_received_chain(msg),
                'body': {
                    'text': self.extract_text_body(msg),
                    'html': self.extract_html_body(msg)
                },
                'attachments': self.extract_attachments(msg)
            }
            
            logger.info(f"Successfully parsed email from {file_path}")
            return parsed_email
            
        except Exception as e:
            logger.error(f"Failed to parse email file {file_path}: {e}")
            raise

    def to_json(self, parsed_email: Dict, output_path: Optional[str] = None) -> str:
        """Convert parsed email to JSON"""
        json_str = json.dumps(parsed_email, indent=2)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(json_str)
            logger.info(f"Saved parsed email to {output_path}")
        
        return json_str
