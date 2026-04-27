<div align="center">

# Plagiarism Detection System

**An intelligent, ML-powered plagiarism checker built with Flask**

*TF-IDF Cosine Similarity · MinHash LSH · Ensemble Scoring · Sentence-Level Analysis*

---

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-black?style=flat-square&logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## Overview

The **Plagiarism Detection System** is a web-based application that analyzes submitted text or uploaded documents and compares them against a local corpus of reference documents. It uses a hybrid unsupervised machine learning approach — combining **TF-IDF cosine similarity** and **MinHash Jaccard similarity** — to produce a reliable ensemble plagiarism score with sentence-level match highlighting.

> Developed by **Group 6 · Wolkite University**

---

## Features

| Feature | Description |
|---|---|
| Document Analysis | Paste full text for document-level plagiarism scanning |
| Sentence Check | Instantly check a single sentence against the entire corpus |
| File Upload | Upload `.txt`, `.pdf`, or `.docx` files for analysis |
| Corpus Management | Add, upload, or remove reference documents via the UI |
| Ensemble Scoring | Combined TF-IDF + MinHash score for higher accuracy |
| Risk Classification | Automatic risk level: Low / Moderate / High / Critical |
| Session History | Track all checks performed during the current session |

---

## How It Works

The detection engine applies two complementary similarity algorithms and combines them into a single ensemble score:

```
Ensemble Score = (0.6 x Cosine Similarity) + (0.4 x Jaccard Similarity)
```

| Algorithm | Weight | Description |
|---|---|---|
| TF-IDF Cosine Similarity | 60% | Measures vocabulary and term-frequency overlap |
| MinHash Jaccard Similarity | 40% | Approximates set-based shingle overlap via LSH |

### Risk Level Thresholds

| Ensemble Score | Risk Level | Interpretation |
|---|---|---|
| < 0.26 | Low | Content appears mostly original |
| 0.26 – 0.50 | Moderate | Some sections may require review |
| 0.51 – 0.75 | High | Significant similarity detected |
| >= 0.76 | Critical | Content is likely plagiarized |

---

## Project Structure

```
PlagiarismChecker/
│
├── app.py                    # Flask application and all API routes
│
├── plagiarism/
│   ├── detector.py           # Core ML detection engine
│   └── __init__.py
│
├── templates/
│   └── index.html            # Web interface (single-page UI)
│
├── static/
│   └── style.css             # Application styling
│
├── corpus/                   # Reference documents (.txt files)
│   ├── document1.txt
│   └── document2.txt
│
├── uploads/                  # Temporary upload directory (auto-created)
│
├── tests/
│   └── test_detector.py      # Unit tests for the detection engine
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web interface |
| `POST` | `/check` | Analyze pasted text for plagiarism |
| `POST` | `/check_sentence` | Check a single sentence against the corpus |
| `POST` | `/upload` | Upload and analyze a file for plagiarism |
| `GET` | `/history` | Retrieve in-memory submission history |
| `GET` | `/corpus` | List all corpus reference documents |
| `POST` | `/corpus` | Add a document via JSON `{ title, text }` |
| `DELETE` | `/corpus` | Remove a document via JSON `{ title }` |
| `POST` | `/corpus/upload` | Upload a file directly into the corpus |

---

## Setup and Installation

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### 1. Clone the repository

```bash
git clone https://github.com/your-username/plagiarism-checker.git
cd plagiarism-checker
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in your browser

```
http://127.0.0.1:5000
```

---

## Usage Guide

### Check Document Tab
- **Upload File** — select a `.txt`, `.pdf`, or `.docx` file and click **Upload & Analyze**
- **Paste Text** — paste any block of text and click **Analyze**
- **Quick Sentence Check** — paste a single sentence and click **Check Sentence**

### Results Tab
- View the ensemble score and risk level
- Inspect per-document match scores with cosine and Jaccard breakdown
- Review flagged sentence pairs with similarity percentages and source attribution

### Corpus Tab
- **Upload File** — add a `.txt`, `.pdf`, or `.docx` directly as a reference document
- **Paste Text** — manually add a document with a custom title
- View word counts and dates for all corpus documents
- Remove any document from the corpus at any time

### History Tab
- Browse all checks performed in the current session
- Click any entry to reload its full results in the Results tab

---

## Running Tests

```bash
pytest tests/
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `Flask` | Web framework and routing |
| `scikit-learn` | TF-IDF vectorization and cosine similarity |
| `datasketch` | MinHash signatures and LSH indexing |
| `nltk` | Tokenization, stopword removal, lemmatization |
| `PyPDF2` | PDF text extraction |
| `python-docx` | DOCX text extraction |

> NLTK resources (`punkt`, `stopwords`, `wordnet`) are downloaded automatically on first run.

---

## Notes

- Submission history is stored in memory only and resets when the server restarts
- The corpus loads `.txt` files from the `corpus/` directory at startup
- Uploaded PDF and DOCX files are extracted to plain text before being saved to the corpus
- For production use, consider replacing in-memory history with a database such as SQLite or PostgreSQL

---

## Future Improvements

- Persistent history storage with a database
- User authentication and per-user corpus management
- Support for additional file formats such as `.odt` and `.rtf`
- Internet-scale detection via external academic APIs
- Exportable plagiarism reports in PDF format

---

<div align="center">

Made with dedication by **Group 6 · Wolkite University**

</div>
