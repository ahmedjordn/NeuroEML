"""
NeuroEML Configuration Settings
Centralized configuration for all modules
"""

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv  # <-- ADD THIS IMPORT

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent

# Load environment variables from .env file
# This looks for a .env file in your project root directory
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")  # <-- ADD THIS LINE

# API Keys & External Services (Now these will successfully read your keys!)
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")

# Ollama Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
OLLAMA_TIMEOUT = 600 # seconds


# AI Analysis Settings
AI_PROFILER_TEMP = 0.3  # Lower temperature for consistent profiling
AI_AUDITOR_TEMP = 0.3   # Lower temperature for technical analysis
AI_MAX_TOKENS = 1000

# Risk Scoring Thresholds
RISK_THRESHOLDS = {
    "critical": 80,
    "high": 60,
    "medium": 40,
    "low": 20,
    "safe": 0
}

# OSINT Settings
VIRUSTOTAL_TIMEOUT = 10
ABUSEIPDB_TIMEOUT = 10
IOC_THRESHOLD_COUNT = 10  # Flag if detected by 10+ engines

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = PROJECT_ROOT / "logs" / "neuroeml.log"

# File Upload
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
TEMP_DIR = PROJECT_ROOT / "temp"

# Database/Cache (for future iterations)
CACHE_RESULTS = True
CACHE_TTL = 3600  # 1 hour

@dataclass
class AnalysisConfig:
    """Configuration for email analysis passes"""
    enable_profiler: bool = True
    enable_auditor: bool = True
    enable_osint: bool = True
    enable_metadata: bool = True
    
    # Regex patterns for extraction
    URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]*'
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    IP_PATTERN = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    HASH_PATTERN = r'(?:[a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64})\b'
