# NeuroEML Architecture

## Overview

NeuroEML is built on a modular pipeline architecture where each component handles a specific analysis domain. Components run in parallel where possible, then results are aggregated for final risk scoring.

## Pipeline Flow

```
.eml File Input
     │
     ▼
┌─────────────┐
│ EmailParser │  ← parsers/email_parser.py
│             │    Extracts: headers, body, attachments
└──────┬──────┘
       │
       ▼ Structured Email Data
┌──────────────────────────────────────────┐
│         Parallel Analysis Engines         │
│                                           │
│  ┌──────────────┐  ┌──────────────────┐  │
│  │IdentityEngine│  │  HeaderEngine    │  │
│  │ (Spoofing)   │  │ (SPF/DKIM/DMARC) │  │
│  └──────────────┘  └──────────────────┘  │
│  ┌──────────────┐                        │
│  │  URLEngine   │                        │
│  │ (Link Scan)  │                        │
│  └──────────────┘                        │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│           AI Dual-Pass Analysis           │
│                                           │
│  ┌──────────────┐  ┌──────────────────┐  │
│  │  AI Profiler │  │   AI Auditor     │  │
│  │ (Psychology) │  │  (Technical)     │  │
│  └──────────────┘  └──────────────────┘  │
│         Both powered by Ollama LLM        │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│            OSINT Enrichment               │
│  ┌──────────────┐  ┌──────────────────┐  │
│  │ VirusTotal   │  │   AbuseIPDB      │  │
│  │ (URL/Hash)   │  │  (IP Reputation) │  │
│  └──────────────┘  └──────────────────┘  │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│         Risk Scoring & Aggregation        │
│    Final Score = Weighted Average of:     │
│    Identity(15%) + Header(15%) +          │
│    URL(15%) + Profiler(20%) +             │
│    Auditor(20%) + OSINT(15%)              │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│          Streamlit Dashboard              │
│   ui/streamlit_app.py                    │
└──────────────────────────────────────────┘
```

## Module Descriptions

### `parsers/email_parser.py`
Handles `.eml` file ingestion. Extracts:
- All headers (routing, authentication, custom)
- Text and HTML body parts
- Attachments with MD5/SHA256 hashes
- Inline images

### `engines/analysis_engines.py`
Three rule-based engines:

**IdentityEngine** — Detects sender spoofing:
- Display name vs. envelope address mismatch
- Punycode/homograph domain detection
- Free email provider impersonation
- Domain alignment (From vs. Reply-To vs. Return-Path)

**HeaderEngine** — Email authentication analysis:
- SPF record validation
- DKIM signature verification
- DMARC policy check
- Hop analysis and IP geolocation
- Reverse DNS verification

**URLEngine** — Link threat analysis:
- URL extraction from HTML and plain text
- HTTP redirect chain following
- IP-based URL detection (bypassing DNS)
- Suspicious TLD and pattern matching
- URL shortener detection

### `engines/ai_analysis.py`
Dual-pass LLM analysis via Ollama:

**AIProfiler** (Pass A - Psychological):
- Urgency and time-pressure detection
- Authority impersonation signals
- Fear and threat appeals
- Social proof manipulation
- Reward/prize lures

**AIAuditor** (Pass B - Technical):
- Hidden HTML elements and iframes
- JavaScript obfuscation
- Base64-encoded payloads
- Credential harvesting form detection
- Exploit kit fingerprints

### `engines/osint_enrichment.py`
External threat intelligence:
- VirusTotal: URL scanning (90+ engines), file hash lookup
- AbuseIPDB: IP reputation and abuse reports
- IOC extraction: IPs, URLs, hashes, email addresses

### `models/analyzer.py`
Main orchestrator (`NeuroEMLAnalyzer`):
- Manages pipeline execution
- Parallel engine execution via `concurrent.futures`
- Aggregates all scores
- Generates recommendations
- Outputs JSON report

### `ui/streamlit_app.py`
Streamlit web dashboard:
- Drag-and-drop `.eml` upload
- Real-time risk gauge (Plotly)
- Tabbed results view
- Export to JSON and CSV

## Data Structures

### Parsed Email
```python
{
    "headers": {"From": "...", "To": "...", ...},
    "body": {"text": "...", "html": "..."},
    "attachments": [{"filename": "...", "md5": "...", "sha256": "..."}]
}
```

### Analysis Report
```python
{
    "metadata": {"analysis_timestamp": "...", "status": "completed"},
    "parsing": {"success": True, "headers_count": N, ...},
    "engines": {
        "identity_engine": {"risk_score": 0-100, ...},
        "header_engine": {"risk_score": 0-100, "spf_status": "...", ...},
        "url_engine": {"risk_score": 0-100, "total_urls": N, ...}
    },
    "ai_analysis": {
        "profiler": {"overall_suspicion_score": 0-100, "tactics": {...}},
        "auditor": {"technical_risk_score": 0-100, "critical_findings": [...]}
    },
    "osint_enrichment": {"flagged_iocs": N, "high_risk_indicators": [...]},
    "final_risk_score": 0-100,
    "risk_level": "CRITICAL|HIGH|MEDIUM|LOW|SAFE",
    "recommendations": [...]
}
```
