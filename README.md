I see exactly what happened! When you copied the text from my last message, your browser copied the *visual* text instead of the underlying Markdown code. All the hashtags (`#`), asterisks (`*`), and backticks (` ` `) that tell GitHub how to format the page got stripped out, leaving you with a giant wall of text.

To fix this, I am putting the exact same README into a **code block** below.

Hover over the top-right corner of the black box below and click the **"Copy code"** button. Then, go back to your GitHub editor, delete that wall of text, and paste this in. It will instantly format perfectly into headings, bullet points, and code blocks.

```markdown
# NeuroEML: Advanced Email Threat Intelligence Platform

NeuroEML is a high-performance, concurrent email security analysis platform designed to detect sophisticated phishing attempts, identity spoofing, and malicious payloads. It combines deterministic security engines with dual-pass local Large Language Model (LLM) inference and real-time Open Source Intelligence (OSINT) enrichment to provide a comprehensive threat profile for any `.eml` file.

## Core Architecture

The platform operates on a six-layer analysis pipeline, optimized for speed using Python's `concurrent.futures.ThreadPoolExecutor`. 

* **Identity Engine**: Detects sender impersonation, display name spoofing, and advanced Punycode/homograph attacks.
* **Header Engine**: Validates SPF, DKIM, and DMARC authentication protocols while mapping the email hop trace to identify originating IPs.
* **URL Engine**: Concurrently extracts, expands, and evaluates all embedded links for malicious patterns and excessive redirect chains.
* **OSINT Enrichment**: Queries VirusTotal and AbuseIPDB in parallel to cross-reference extracted domains, IPs, and file hashes against global threat intelligence databases.
* **AI Profiler (Psychological)**: Utilizes local LLM inference to identify social engineering tactics, including urgency, fear appeals, and false authority.
* **AI Auditor (Technical)**: Analyzes raw HTML bodies via LLM to detect technical obfuscation, hidden tracking pixels, base64 payloads, and credential harvesting forms.

## Technology Stack

* **Frontend**: Streamlit (Custom "Aurora" Glassmorphism UI)
* **Concurrency**: Native Python Threading (`ThreadPoolExecutor`) for I/O-bound API and URL resolution tasks.
* **AI Inference**: Ollama (Local LLM execution for data privacy and zero-cost inference).
* **Threat Intelligence APIs**: VirusTotal API v3, AbuseIPDB API v2.

## Prerequisites

Before installing NeuroEML, ensure you have the following installed on your system:
* Python 3.9 or higher
* [Ollama](https://ollama.com/) (running locally)
* Active API keys for VirusTotal and AbuseIPDB

## Installation

1. **Clone the repository**
```bash
git clone [https://github.com/ahmedjordn/NeuroEML.git](https://github.com/ahmedjordn/NeuroEML.git)
cd NeuroEML

```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

```

3. **Install dependencies**

```bash
pip install -r requirements.txt

```

4. **Pull the required LLM via Ollama**
For optimal speed and accuracy, a smaller, highly capable model is recommended.

```bash
ollama pull phi3

```

## Configuration

Create a `.env` file in the root directory of the project. Do not use `.env.txt`. The application relies on `python-dotenv` to load these credentials securely into the environment prior to runtime.

```env
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3
OLLAMA_TIMEOUT=600

```

## Usage

1. Ensure the Ollama service is running in the background.
2. Start the Streamlit dashboard:

```bash
streamlit run ui/streamlit_app.py

```

3. Navigate to `http://localhost:8501` in your web browser.
4. Upload an `.eml` file using the sidebar interface. The application will immediately process the file across all concurrent engines and display the final security report.

## Export Capabilities

NeuroEML supports comprehensive reporting. Upon completion of an analysis, users can export:

* **JSON Report**: A complete, structured output of all engine findings, AI summaries, and calculated risk scores.
* **IOCs CSV**: A formatted list of all High-Risk Indicators of Compromise (IPs, Hashes, and URLs) flagged by the OSINT modules.

## Disclaimer

This tool is designed for authorized security testing, incident response, and educational purposes only. Users are responsible for ensuring compliance with applicable laws and regulations regarding data privacy and API usage limits.

```

```
