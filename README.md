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
