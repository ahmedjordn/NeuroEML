## 🚀 NeuroEML - Quick Start Guide

### 5-Minute Setup

#### Option 1: Local Installation (Recommended)

```bash
# 1. Navigate to project
cd NeuroEML

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Start Ollama (in another terminal)
ollama serve
# In another terminal: ollama pull mistral

# 4. Copy environment template
cp .env.example .env
# Edit .env with your API keys (optional for basic testing)

# 5. Run dashboard
streamlit run ui/streamlit_app.py
```

**✅ Done!** Open browser to `http://localhost:8501`

---

#### Option 2: Docker (All-in-One)

```bash
# 1. Build images
docker-compose build

# 2. Start services
docker-compose up -d

# 3. Wait for Ollama to download model (first time)
docker logs neuroeml_ollama -f

# 4. Access dashboard
# http://localhost:8501
```

---

### First Analysis

1. **Get Test Email**
   - Use any `.eml` file or export from your email client
   - Right-click email → "Export as EML" (Outlook)
   - Or use Gmail's download feature

2. **Upload via Dashboard**
   - Open Streamlit UI
   - Click "Upload .eml file" in sidebar
   - Select your email file
   - Wait for analysis (10-30 seconds)

3. **Review Results**
   - **Risk Score:** 0-100 gauge showing threat level
   - **Components:** Individual engine scores
   - **Email Analysis:** Headers, authentication status
   - **URLs:** Link analysis with redirects
   - **AI Analysis:** Profiler & Auditor insights
   - **OSINT:** Threat intelligence findings
   - **Recommendations:** Actionable security steps

4. **Export Report**
   - Download JSON for detailed analysis
   - Export CSV of high-risk IOCs
   - Share with security team

---

### Configuration (Optional)

#### Add VirusTotal API (For OSINT)

1. Get free API key: https://www.virustotal.com/
2. Add to `.env`:
   ```
   VIRUSTOTAL_API_KEY=your_key_here
   ```
3. Restart app (Ctrl+C → streamlit run ui/streamlit_app.py)

#### Change AI Model

In `.env`:
```
OLLAMA_MODEL=mistral          # Fast, recommended
OLLAMA_MODEL=neural-chat      # Good for security
OLLAMA_MODEL=dolphin-mixtral  # Higher quality
```

Then pull model:
```bash
ollama pull neural-chat
```

---

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Ollama not found" | Run `ollama serve` in another terminal |
| Slow analysis | Use faster model: `OLLAMA_MODEL=mistral` |
| Import errors | Run `pip install -r requirements.txt` |
| Port 8501 in use | Kill other Streamlit: `lsof -i :8501` then `kill -9 <PID>` |
| Out of memory | Close other apps or reduce model size |

---

### Project Structure

```
NeuroEML/
├── parsers/          → Email parsing logic
├── engines/          → Analysis engines (Identity, Header, URL, AI, OSINT)
├── models/           → Main orchestrator (analyzer.py)
├── ui/               → Streamlit dashboard
├── config/           → Settings and configuration
├── requirements.txt  → Python packages
├── .env             → API keys (create from .env.example)
└── docker-compose.yml → Docker setup
```

---

### Use Cases

#### 1. Phishing Analysis
```
Upload suspicious email → NeuroEML analyzes → Get risk score
→ Share report with team → Block/quarantine if needed
```

#### 2. Security Training
```
Send suspicious emails to NeuroEML → Review detailed breakdown
→ Train users on red flags identified by AI
```

#### 3. Threat Investigation
```
Collect emails from incident → Batch analyze with tool
→ Extract IOCs → Cross-reference with threat intel
```

#### 4. Email Gateway Testing
```
Test gateway filters with known-bad emails
→ Use NeuroEML to verify detections
```

---

### Key Metrics Explained

| Metric | What It Means |
|--------|---------------|
| **Risk Score** | 0-100: Overall threat level (higher = worse) |
| **SPF/DKIM/DMARC** | Authentication results (PASS is good) |
| **Punycode** | Domain spoofing using Unicode (homograph attack) |
| **Social Engineering Score** | Psychological manipulation tactics (urgency, fear, etc.) |
| **Technical Risk** | Obfuscation, malware indicators, exploit code |
| **OSINT Hits** | How many threat databases flagged URLs/IPs |

---

### Next Steps

1. **Create baseline:** Analyze legitimate emails to understand normal scores
2. **Set thresholds:** Decide your organization's risk tolerance
3. **Integrate:** Connect with email gateway/SIEM
4. **Train team:** Show analysts how to use NeuroEML
5. **Iterate:** Adjust prompts/rules based on findings

---

### Need Help?

- **Errors?** Check project logs: `tail -f logs/neuroeml.log`
- **Questions?** Review README.md
- **Customize?** Edit prompts in `engines/ai_analysis.py`
- **Extend?** Add new engines or APIs to `engines/` folder

---

### Performance Expectations

| Component | Time |
|-----------|------|
| Email parsing | < 1 second |
| Identity/Header/URL engines | < 2 seconds |
| AI Profiler pass | 5-10 seconds |
| AI Auditor pass | 8-15 seconds |
| OSINT enrichment | 3-5 seconds (if APIs configured) |
| **Total** | **10-30 seconds** |

(Times vary based on email size and model choice)

---

**Ready to analyze?** 🚀

```bash
streamlit run ui/streamlit_app.py
```

Then upload your first `.eml` file and see the magic happen! ✨
