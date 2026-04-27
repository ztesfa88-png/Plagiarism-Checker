# Plagiarism Checker

A Flask-based plagiarism detection application that compares submitted text and uploaded files against a local corpus of documents using unsupervised ML techniques.

## Features

- Paste text for full document-level plagiarism analysis
- Quick single-sentence check against the corpus
- Upload `.txt`, `.pdf`, or `.docx` files for scanning
- Upload files directly into the corpus as reference documents
- Add or remove corpus documents via the UI
- Sentence-level match highlighting with source attribution
- Risk scoring: Low / Moderate / High / Critical
- Submission history tracked in memory during the session

## How it works

The app combines two similarity methods into an ensemble score:

- **TF-IDF cosine similarity** (60% weight) — measures vocabulary overlap between documents
- **MinHash Jaccard similarity** (40% weight) — approximates set-based overlap using LSH for fast candidate retrieval
- **Ensemble score** = `0.6 × cosine + 0.4 × jaccard`

Risk levels are assigned based on the ensemble score:

| Score     | Risk Level |
|-----------|------------|
| < 0.26    | Low        |
| 0.26–0.50 | Moderate   |
| 0.51–0.75 | High       |
| ≥ 0.76    | Critical   |

## Project structure

```
├── app.py                  # Flask app and all API routes
├── plagiarism/
│   ├── detector.py         # Core detection engine
│   └── __init__.py
├── templates/
│   └── index.html          # Frontend UI
├── static/
│   └── style.css           # Styling
├── corpus/                 # Reference documents (.txt)
├── uploads/                # Temporary upload folder (auto-created)
├── tests/
│   └── test_detector.py    # Unit tests
└── requirements.txt
```

## API routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Serves the web UI |
| POST | `/check` | Check pasted text for plagiarism |
| POST | `/check_sentence` | Check a single sentence against corpus |
| POST | `/upload` | Upload a file and check it for plagiarism |
| GET | `/history` | Return in-memory submission history |
| GET | `/corpus` | List all corpus documents |
| POST | `/corpus` | Add a document to corpus (JSON: title + text) |
| DELETE | `/corpus` | Remove a document from corpus (JSON: title) |
| POST | `/corpus/upload` | Upload a file directly into the corpus |

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open in your browser: `http://127.0.0.1:5000`

## Usage

### Check Document tab
- **Upload File** — upload a `.txt`, `.pdf`, or `.docx` to scan it against the corpus
- **Paste text** — paste any text and click **Analyze**
- **Quick Sentence Check** — paste a single sentence and click **Check Sentence**

### Results tab
- Ensemble score and risk level
- Per-document match scores (cosine + Jaccard breakdown)
- Flagged sentence pairs with similarity percentages

### Corpus tab
- **Upload File** — upload a `.txt`, `.pdf`, or `.docx` to add it as a reference document
- **Paste text** — paste text with a title to add it manually
- View and remove existing corpus documents

### History tab
- Lists all checks performed in the current session
- Click any entry to view its full results

## Running tests

```bash
pytest tests/
```

## Notes

- History is stored in memory and resets when the server restarts
- The corpus only loads `.txt` files from disk at startup; uploaded PDF/DOCX files are extracted to text before being saved
- NLTK resources (`punkt`, `stopwords`, `wordnet`) are downloaded automatically on first run
- PDF support requires `PyPDF2`, DOCX support requires `python-docx` — both included in `requirements.txt`
