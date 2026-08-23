# COPAN — Classification-Oriented Phishing Analysis Network

> Agentic AI phishing detector built on a dual-engine MCO architecture.  
> Research paper: *Loo, Galindo, Romero et al.* — Universidad Tecnológica de Honduras (UTH), 2025.

---

## What is COPAN?

COPAN is an end-to-end phishing detection system that combines transformer-based natural language understanding with structural email analysis. It classifies emails as **Phishing**, **Suspicious**, or **Legitimate**, provides confidence scores, explains its reasoning, and autonomously recommends an action (Quarantine / Alert / Pass).

The system is built around the **MCO loop** — Monitor → Classify → Optimize — enabling continuous self-improvement through labeled feedback and retraining.

---

## Architecture

```
Email Input (.eml / Text / Screenshot)
        │
        ├─── ENGINE A: Semantic Understanding
        │       DistilBERT 768-dim [CLS] embedding
        │       + rule-based pattern scoring
        │       (urgency, authority, credential harvesting, pressure)
        │
        ├─── ENGINE B: Structural Analysis
        │       URL analysis & typosquatting (45+ brands)
        │       SPF / DKIM / DMARC header validation
        │       HTML hidden elements, forms, tracking pixels
        │       Sender spoofing detection
        │
        └─── FEATURE FUSION → Random Forest (84-dim vector)
                │
                └─── Verdict + Confidence + Explanation + Action
```

**Key metrics (validation on 82,500 emails — Enron, Ling, SpamAssassin corpora):**

| Metric | Value |
|---|---|
| Accuracy | 92.5% |
| False Negative Rate | 6.25% |
| False Positive Rate | 1.25% |

---

## Features

- **Dual-engine analysis** — semantic NLP (DistilBERT) + structural heuristics (URLs, headers, HTML)
- **Three input modes** — upload `.eml`, paste raw text, or upload a screenshot (OCR via Tesseract)
- **Explainability** — per-indicator scores, human-readable explanation, education note
- **Raw features panel** — full technical feature dump for research/debugging
- **KPI dashboard** — detection rates, average confidence, indicator distribution charts
- **Scan history** — searchable log with CSV export
- **Security Advisor** — Claude-powered chat that auto-explains every verdict in plain language
- **Adversarial robustness** — rate limiting, input normalization, training data integrity checks
- **Retraining pipeline** — label feedback loop with high-confidence quarantine for suspicious labels

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.10+ / FastAPI / Uvicorn |
| NLP Model | DistilBERT (HuggingFace Transformers) |
| Classifier | Random Forest (scikit-learn) |
| Deep Learning | PyTorch |
| OCR | Tesseract + Pillow |
| Database | SQLite (persistent scan log) |
| Frontend | Tailwind CSS / Vanilla JS |
| URL Analysis | tldextract / Levenshtein |
| AI Chat | Claude API (Anthropic) |

---

## Installation

### Prerequisites

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and on PATH (for screenshot analysis)

### Setup

```bash
# Clone the repository
git clone https://github.com/AlbertoGTHN/COPAN.git
cd COPAN

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Train the classifier

The trained model files (`.pkl`) are not included in the repository (large binaries). Generate them from the Enron/SpamAssassin datasets:

```bash
python train_datasets.py
```

---

## Running COPAN

### Windows (recommended)

Double-click `start_copan.cmd` or run:

```bash
start_copan.cmd
```

This sets `EXPOSE_RAW_FEATURES=true` and starts the server.

### Manual start

```bash
set EXPOSE_RAW_FEATURES=true        # Windows
# export EXPOSE_RAW_FEATURES=true   # macOS/Linux

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000** in your browser.

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `EXPOSE_RAW_FEATURES` | Include raw feature dict in API responses | `false` |
| `ANTHROPIC_API_KEY` | Pre-configure Claude API key for the Security Advisor chat | *(none)* |
| `DETECTOR_ADMIN_KEY` | Protect training endpoints in production | *(empty = open)* |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analyze/eml` | Analyze an uploaded `.eml` file |
| `POST` | `/api/analyze/text` | Analyze raw text (JSON body) |
| `POST` | `/api/analyze/screenshot` | Analyze a screenshot via OCR |
| `GET` | `/api/history` | Retrieve scan history |
| `GET` | `/api/stats` | KPI statistics |
| `POST` | `/api/chat` | Security Advisor chat (requires Anthropic key) |
| `GET` | `/api/config` | Public server configuration flags |

### Text analysis example

```bash
curl -X POST http://127.0.0.1:8000/api/analyze/text \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Urgent: verify your account",
    "body": "Click here immediately or your account will be suspended.",
    "sender": "security@paypal-verify.net",
    "urls": ["http://paypal-verify.net/login"]
  }'
```

---

## Test Suite

The `tests/` directory contains two email sets for evaluating the model:

- **`tests/eml/`** — A01–A100: 50 phishing + 50 legitimate emails covering common adversarial techniques (homoglyphs, zero-width characters, thread hijacking, content padding, calm-tone evasion)
- **`tests/PrompInjection/`** — PI-01–PI-10: prompt injection attack emails targeting the AI Security Advisor (white-on-white CSS, JSON metadata injection, HTML comment role assignment, XML delimiter injection, few-shot override, system prompt injection)

---

## Security Mitigations

| ID | Mitigation | Description |
|---|---|---|
| V-01 | Admin key auth | Training endpoints protected by `DETECTOR_ADMIN_KEY` |
| V-02 | Rate limiting | `/api/analyze/*` — 30 req/min per IP |
| V-03 | Rate limiting | `/api/train/*` — 5 req/min per IP |
| V-04 | Feature stripping | `raw_features` hidden unless `EXPOSE_RAW_FEATURES=true` |
| V-05 | Unicode normalization | NFKC normalization in all parsers |
| V-06 | Training integrity | Mislabeled high-confidence samples quarantined before retraining |

---

## Research

This system is the implementation artifact for the paper:

> **"Adversarial Robustness of COPAN — Classification-Oriented Phishing Analysis Network"**  
> Loo, Galindo, Romero et al.  
> Universidad Tecnológica de Honduras (UTH), 2025  
> Submitted to LACCI '26

The paper proposes moving beyond rule-based systems (EBIDS) toward an agentic architecture capable of autonomous monitoring, intelligent classification, and continuous self-optimization. The system was validated on 82,500 emails from the Enron, Ling, and SpamAssassin corpora.

---

## Authors

- Alberto Galindo — [albertogthn@gmail.com](mailto:albertogthn@gmail.com)
- Loo, Romero et al. — Universidad Tecnológica de Honduras (UTH)

---

## License

For academic and research use. See [SECURITY.md](SECURITY.md) for responsible disclosure guidelines.
