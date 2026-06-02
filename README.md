# NeuroEML: Advanced Email Threat Intelligence Platform

NeuroEML is a high-performance, concurrent email security analysis platform designed to detect sophisticated phishing attempts, identity spoofing, and malicious payloads. It combines deterministic security engines with dual-pass local Large Language Model (LLM) inference and real-time Open Source Intelligence (OSINT) enrichment to provide a comprehensive threat profile for any `.eml` file.

---

## Core Architecture

The platform operates on a six-layer analysis pipeline, optimized for speed using Python's `concurrent.futures.ThreadPoolExecutor`.

### Identity Engine

Detects sender impersonation, display name spoofing, and advanced Punycode/homograph attacks.

### Header Engine

Validates SPF, DKIM, and DMARC authentication protocols while mapping the email hop trace to identify originating IPs.

### URL Engine

Concurrently extracts, expands, and evaluates all embedded links for malicious patterns and excessive redirect chains.

### OSINT Enrichment

Queries VirusTotal and AbuseIPDB in parallel to cross-reference extracted domains, IPs, and file hashes against global threat intelligence databases.

### AI Profiler (Psychological)

Utilizes local LLM inference to identify social engineering tactics, including urgency, fear appeals, and false authority.

### AI Auditor (Technical)

Analyzes raw HTML bodies via LLM to detect technical obfuscation, hidden tracking pixels, base64 payloads, and credential harvesting forms.

---

## Technology Stack

* **Frontend:** Streamlit (Custom "Aurora" Glassmorphism UI)
* **Concurrency:** Native Python Threading (`ThreadPoolExecutor`) for I/O-bound API and URL resolution tasks
* **AI Inference:** Ollama (Local LLM execution for data privacy and zero-cost inference)
* **Threat Intelligence APIs:** VirusTotal API v3, AbuseIPDB API v2

---

## Prerequisites

Before installing NeuroEML, ensure you have the following installed on your system:

* Python 3.9 or higher
* Ollama (running locally)
* Active API keys for VirusTotal and AbuseIPDB

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ahmedjordn/NeuroEML.git
cd NeuroEML
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull the Required LLM via Ollama

For optimal speed and accuracy, a smaller, highly capable model is recommended.

```bash
ollama pull phi3
```

---

## Configuration

Create a `.env` file in the root directory of the project. Do not use `.env.txt`.

The application relies on `python-dotenv` to securely load credentials into the environment prior to runtime.

```env
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3
OLLAMA_TIMEOUT=600
```

---

## Usage

### 1. Ensure Ollama is Running

Start the Ollama service in the background.

### 2. Launch the Dashboard

```bash
streamlit run ui/streamlit_app.py
```

### 3. Open the Application

Navigate to:

```text
http://localhost:8501
```

### 4. Analyze an Email

Upload an `.eml` file using the sidebar interface.

The application will immediately process the file across all concurrent engines and display the final security report.

---

## Export Capabilities

NeuroEML supports comprehensive reporting.

Upon completion of an analysis, users can export:

### JSON Report

A complete, structured output containing:

* Engine findings
* AI analysis results
* Risk scores
* OSINT enrichment data

### IOCs CSV

A formatted list of all high-risk Indicators of Compromise (IOCs), including:

* IP Addresses
* URLs
* File Hashes

Flagged by the OSINT enrichment modules.

---

## Disclaimer

This tool is designed for authorized security testing, incident response, and educational purposes only.

Users are responsible for ensuring compliance with applicable laws, regulations, data privacy requirements, and API usage limitations.
