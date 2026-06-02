# NeuroEML 🧠
## Intelligent Email Security & Threat Analysis Platform

**NeuroEML** is a comprehensive email security analysis tool designed for security professionals. It combines advanced parsing, behavioral AI analysis, threat intelligence enrichment, and forensic capabilities to detect sophisticated email threats.

---

## 🎯 Features

### Core Analysis Components

1. **Email Parser** - Extracts structured data from .eml files
   - Headers (routing, authentication)
   - Body text & HTML
   - Attachments with hashing

2. **Identity Engine** - Detects spoofing and impersonation
   - Display name vs. actual address analysis
   - Punycode/homograph attack detection
   - Domain alignment checks

3. **Header Engine** - Validates email authentication
   - SPF/DKIM/DMARC verification
   - Hop trace and IP analysis
   - Reverse DNS lookups

4. **URL Engine** - Analyzes links and redirects
   - URL expansion and redirect chain detection
   - Suspicious pattern identification
   - IP-based URL detection

5. **AI Profiler** (Dual-Pass #1) - Psychological analysis
   - Urgency/pressure tactics detection
   - Authority/impersonation signals
   - Fear appeals and social engineering patterns
   - Uses Ollama local LLM

6. **AI Auditor** (Dual-Pass #2) - Technical analysis
   - Hidden elements and iframes detection
   - JavaScript obfuscation and base64 encoding
   - Credential harvesting patterns
   - Exploit kit indicators
   - Uses Ollama local LLM

7. **OSINT Enrichment** - External threat intelligence
   - VirusTotal API integration (URLs, hashes)
   - AbuseIPDB API integration (IP reputation)
   - Cross-reference with global threat databases

8. **Risk Scoring** - Comprehensive assessment
   - Multi-layered scoring (6 components)
   - Weighted risk calculation
   - Risk level categorization (CRITICAL/HIGH/MEDIUM/LOW/SAFE)

9. **Professional Dashboard** - Streamlit UI
   - Real-time risk visualization
   - Interactive analysis results
   - Export capabilities (JSON, CSV)
   - SOC-analyst friendly interface

---

## 📋 System Architecture

```
EML File
  ↓
[Email Parser] → Structured JSON
  ↓
┌─────────────────────────────────┐
│   Parallel Analysis Engines     │
├─────────────────────────────────┤
│ Identity Engine    │ Header Engine │ URL Engine
│ (Spoofing)         │ (Auth Check)  │ (Link Analysis)
└─────────────────────────────────┘
  ↓
[AI Dual-Pass Analysis]
  ├─ Profiler (Psychological) → Ollama
  └─ Auditor (Technical) → Ollama
  ↓
[OSINT Enrichment]
  ├─ VirusTotal (URLs, Hashes)
  └─ AbuseIPDB (IPs)
  ↓
[Risk Scoring & Recommendations]
  ↓
[Streamlit Dashboard]
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Ollama (with model like `mistral` or `neural-chat`)
- VirusTotal API key (optional, for OSINT)
- AbuseIPDB API key (optional, for OSINT)

### Setup

1. **Clone/Extract Project**
```bash
cd NeuroEML
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
Create `.env` file in project root:
```
VIRUSTOTAL_API_KEY=your_api_key_here
ABUSEIPDB_API_KEY=your_api_key_here
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral
```

4. **Start Ollama** (separate terminal)
```bash
ollama serve
ollama pull mistral  # Or your preferred model
```

5. **Run Streamlit Dashboard**
```bash
streamlit run ui/streamlit_app.py
```

The app will open at `http://localhost:8501`

---

## 📖 Usage

### Via Streamlit Dashboard (Recommended)

1. Start the app: `streamlit run ui/streamlit_app.py`
2. Upload `.eml` file via sidebar
3. View comprehensive analysis with:
   - Risk score gauge
   - Component analysis breakdown
   - Email header details
   - URL analysis with screenshots
   - AI profiler & auditor results
   - OSINT enrichment findings
   - Security recommendations
4. Export results as JSON or CSV

### Via Command Line

```bash
python models/analyzer.py email.eml output_report.json
```

### Programmatic Usage

```python
from models.analyzer import run_analysis

# Analyze email
report = run_analysis("email.eml", output_json="report.json")

# Access results
risk_score = report['final_risk_score']
risk_level = report['risk_level']
recommendations = report['recommendations']

# Print recommendations
for rec in recommendations:
    print(rec)
```

---

## 🔧 Configuration

Edit `config/settings.py` for:
- AI model selection
- Risk scoring thresholds
- OSINT API keys
- Logging levels
- File size limits
- Regex patterns for IOC extraction

---

## 📊 Risk Scoring

**Final Risk Score** = Weighted combination of:

| Component | Weight | Measures |
|-----------|--------|----------|
| Identity Engine | 15% | Spoofing, homographs, domain alignment |
| Header Engine | 15% | SPF/DKIM/DMARC validation, IP analysis |
| URL Engine | 15% | Suspicious links, redirects, IP-based URLs |
| AI Profiler | 20% | Psychological manipulation tactics |
| AI Auditor | 20% | Technical obfuscation, malware indicators |
| OSINT | 15% | Threat intelligence hits |

**Risk Levels:**
- 🚨 **CRITICAL** (80-100): Immediate threat
- ⚠️ **HIGH** (60-79): Significant risk
- ⚡ **MEDIUM** (40-59): Suspicious patterns
- ✓ **LOW** (20-39): Minor concerns
- ✅ **SAFE** (0-19): Likely legitimate

---

## 🔐 OSINT Integration

### VirusTotal
- Check file hashes (MD5, SHA256)
- Analyze URLs against 90+ security vendors
- Returns detection ratio and categories

### AbuseIPDB
- Check IP reputation
- Get abuse confidence scores
- View report categories

**Note:** Requires API keys from respective services.

---

## 🧠 AI Models

### Ollama Integration

Tested models:
- **mistral** (7B) - Recommended, best balance
- **neural-chat** (7B) - Good for security analysis
- **dolphin-mixtral** (8x7B) - Higher quality, more resource intensive
- **llama2** (7B) - Fast, lighter

### Custom Prompts

Edit prompts in:
- `engines/ai_analysis.py` - AIProfiler & AIAuditor templates

---

## 📁 Project Structure

```
NeuroEML/
├── config/
│   └── settings.py              # Configuration
├── parsers/
│   └── email_parser.py          # EML parsing logic
├── engines/
│   ├── analysis_engines.py      # Identity, Header, URL engines
│   ├── ai_analysis.py           # AI Profiler & Auditor
│   └── osint_enrichment.py      # VirusTotal & AbuseIPDB
├── models/
│   └── analyzer.py              # Main orchestrator
├── ui/
│   └── streamlit_app.py         # Dashboard UI
├── utils/
│   └── helpers.py               # Utility functions
├── tests/
│   └── test_*.py                # Test suite
├── docs/
│   └── architecture.md          # Detailed documentation
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md                    # This file
```

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test specific module
pytest tests/test_parser.py -v
```

---

## 🛡️ Security Considerations

- **Sandboxed Analysis:** URLs not actually visited (using requests HEAD)
- **Local LLM:** AI analysis runs locally via Ollama (no cloud data transmission)
- **API Key Management:** Use `.env` for sensitive keys
- **Rate Limiting:** Implement request throttling for external APIs
- **File Handling:** Temporary files cleaned up after analysis

---

## 📈 Performance

- **Single email:** 10-30 seconds (depends on content & model)
- **Ollama response time:** 5-15 seconds per AI pass
- **Dashboard:** Real-time rendering with Streamlit
- **Memory:** ~2-4GB (including Ollama model)

---

## 🐛 Troubleshooting

### Ollama Not Connecting
```
Error: Failed to connect to Ollama at http://localhost:11434
```
**Solution:** Ensure Ollama is running: `ollama serve`

### AI Analysis Timeout
```
Error: Ollama request timed out after 120s
```
**Solution:** Increase `OLLAMA_TIMEOUT` in `config/settings.py` or use a faster model

### Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

### VirusTotal API Errors
```
Error: API returned status 403
```
**Solution:** Check API key in `.env`, may have quota limits

---

## 📝 Example Analysis Report

```json
{
  "metadata": {
    "analysis_timestamp": "2024-01-15T10:30:00",
    "file_path": "phishing.eml",
    "status": "completed"
  },
  "final_risk_score": 87,
  "risk_level": "CRITICAL",
  "parsing": {
    "success": true,
    "headers_count": 25,
    "attachments_count": 1,
    "has_html_body": true
  },
  "engines": {
    "identity_engine": {
      "is_spoofing_attempt": true,
      "risk_score": 45
    },
    "header_engine": {
      "spf_status": "fail",
      "dkim_status": "fail",
      "auth_risk_score": 60
    },
    "url_engine": {
      "total_urls": 3,
      "overall_risk_score": 75
    }
  },
  "ai_analysis": {
    "profiler": {
      "overall_suspicion_score": 85,
      "tactics": {
        "urgency": {"score": 9, "indicators": ["URGENT", "ACT NOW"]},
        "fear": {"score": 8, "indicators": ["account suspended"]}
      }
    },
    "auditor": {
      "technical_risk_score": 72,
      "critical_findings": ["Hidden iframe detected", "Form exfiltration attempt"]
    }
  },
  "osint_enrichment": {
    "flagged_iocs": 2,
    "high_risk_indicators": [
      {"type": "url", "value": "http://evil.com/phish", "detections": 45}
    ]
  },
  "recommendations": [
    "🚨 CRITICAL: Block sender immediately",
    "🔴 Punycode domain detected - likely homograph attack",
    "📧 SPF authentication failed - email may be spoofed",
    "🔒 Technical analysis detected suspicious patterns"
  ]
}
```

---

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Machine learning model integration
- Batch processing pipeline
- Database backend (SQLite/PostgreSQL)
- REST API wrapper
- Mobile dashboard
- Advanced threat hunting features

---

## 📜 License

MIT License - See LICENSE file for details

---

## ⚖️ Disclaimer

**NeuroEML** is designed for authorized security testing and analysis only. Ensure you have proper authorization before analyzing emails. Unauthorized access to emails is illegal.

Use responsibly. 🔐

---

## 📞 Support & Documentation

- **Architecture Details:** See `docs/architecture.md`
- **API Reference:** See inline code documentation
- **Issue Reporting:** Create GitHub issue
- **Questions:** Check docs/ folder

---

**Built for Security Professionals** 🛡️

Last Updated: June 2026
