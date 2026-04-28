<div align="center">

---

## <img width="109" height="96" alt="image" src="https://github.com/user-attachments/assets/c7239e10-61c0-466f-8f6e-5ab695f72cbd" />

**College of Computing and Informatics**
<br/>
**Department of Software Engineering**
<br/>
*Fundamentals of Artificial Intelligence*
<br/>
*SEng9132 · 3rd Year*
<br/>
Academic Year and Semester: **2018, Semester 2**

<br/>

### 👥 Members

| # | Name | ID |
|:--:|:--|:--|
| 1 | Zelalem Tesfa | NSR/0868/16 |
| 2 | Samir Gebi | NSR/0673/16 |
| 3 | Temesgen Teka | NSR/1007/16 |
| 4 | Ysmalem Temesgen | NSR/0843/16 |
| 5 | Yohannes Girma | NSR/0850/16 |
| 6 | Yonas Abera | NSR/0857/16 |
| 7 | Temesgen Demeke | NSR/0765/16 |

<br/>

**Submitted to:** Mr. Belay
<br/>
**Submission Date:** 30/08/2018

---

# Plagiarism Detection System

### An intelligent, ML-powered plagiarism checker built with Flask

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1%2B-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-3.9%2B-4B8BBE?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

<br/>

> 🎓 Developed by **Group 6 · Wolkite University**

</div>

---

## 📌 Overview

The **Plagiarism Detection System** is a web-based application that analyzes submitted text or uploaded documents and compares them against a local corpus of reference documents **or directly against each other**.

It uses a **hybrid unsupervised machine learning approach** — combining **TF-IDF Cosine Similarity** and **MinHash Jaccard Similarity** — to produce a reliable ensemble plagiarism score with sentence-level match highlighting.

---

## ✨ Features

| Feature | Description |
|:--|:--|
| 📄 **Document Analysis** | Paste full text for document-level plagiarism scanning |
| 🔍 **Sentence Check** | Instantly check a single sentence against the entire corpus |
| 📁 **Multiple File Upload** | Upload multiple `.txt`, `.pdf`, or `.docx` files at once |
| 🔀 **File-to-File Comparison** | Compare uploaded files against each other — works without a corpus |
| 🗂️ **Corpus Management** | Add, upload, or remove reference documents via the UI |
| 🧠 **Ensemble Scoring** | Combined TF-IDF + MinHash score for higher accuracy |
| 🚦 **Risk Classification** | Automatic risk level: `Low` / `Moderate` / `High` / `Critical` |
| 📊 **Session History** | Track all checks performed during the current session |
| ⚠️ **Empty Corpus Warning** | Visual alert when no reference documents are loaded |

---

## ⚙️ How It Works

The detection engine applies two complementary similarity algorithms and combines them into a single ensemble score:

```
Ensemble Score = (0.6 × Cosine Similarity) + (0.4 × Jaccard Similarity)
```

| Algorithm | Weight | Description |
|:--|:--:|:--|
| **TF-IDF Cosine Similarity** | 60% | Measures vocabulary and term-frequency overlap |
| **MinHash Jaccard Similarity** | 40% | Approximates set-based shingle overlap via LSH |

### 🚦 Risk Level Thresholds

| Ensemble Score | Risk Level | Interpretation |
|:--:|:--:|:--|
| `< 0.26` | 🟢 **Low** | Content appears mostly original |
| `0.26 – 0.50` | 🟡 **Moderate** | Some sections may require review |
| `0.51 – 0.75` | 🟠 **High** | Significant similarity detected |
| `≥ 0.76` | 🔴 **Critical** | Content is likely plagiarized |

### 🔬 Text Preprocessing Pipeline

Each document goes through this pipeline before comparison:

1. **Lowercase** — normalize case
2. **Tokenization** — extract words using regex `\b\w+\b`
3. **Stopword Removal** — remove common English words (the, is, at, etc.)
4. **Lemmatization** — reduce words to base form
5. **Shingling** — create overlapping 3-word sequences for MinHash

---

## 🗂️ Project Structure

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
│   ├── document1.txt         # Seed: plagiarism checker description
│   └── document2.txt         # Seed: system usage description
│
├── uploads/                  # Temporary upload directory (auto-created)
│
├── tests/
│   └── test_detector.py      # Unit tests for the detection engine
│
├── requirements.txt          # Python dependencies (pinned versions)
├── .gitignore
└── README.md
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|:--:|:--|:--|
| `GET` | `/` | Serves the web interface |
| `POST` | `/check` | Analyze pasted text against corpus |
| `POST` | `/check_sentence` | Check a single sentence against the corpus |
| `POST` | `/upload` | Upload multiple files and check against corpus |
| `POST` | `/compare` | Compare multiple files against each other (no corpus needed) |
| `GET` | `/history` | Retrieve in-memory submission history |
| `GET` | `/corpus` | List all corpus reference documents |
| `POST` | `/corpus` | Add a document via JSON `{ title, text }` |
| `DELETE` | `/corpus` | Remove a document via JSON `{ title }` |
| `POST` | `/corpus/upload` | Upload a file directly into the corpus |

---

## 🚀 Setup and Installation

### Prerequisites

- Python **3.9** or higher
- `pip` package manager

### 1. Clone the Repository

```bash
git clone https://github.com/ztesfa88-png/Plagiarism-Checker.git
cd Plagiarism-Checker
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Core only (no PDF/DOCX support)
pip install Flask>=3.1.3 scikit-learn>=1.8.0 datasketch>=1.10.0 nltk>=3.9.4 werkzeug>=3.1.8

# Full install including PDF and DOCX support
pip install Flask>=3.1.3 scikit-learn>=1.8.0 datasketch>=1.10.0 nltk>=3.9.4 werkzeug>=3.1.8 PyPDF2>=3.0.1 python-docx>=1.2.0
```

> `PyPDF2` and `python-docx` are **optional**. Without them the app still works, but PDF/DOCX uploads will return an error message.

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Your Browser

```
http://127.0.0.1:5000
```

---

## 🖥️ Usage Guide

### 📄 Check Document Tab

#### Upload Files
- Select one or more `.txt`, `.pdf`, or `.docx` files (max 16MB each)
- **"Check vs Corpus"** — checks each file against the corpus
- **"Compare Files"** — compares files against each other (no corpus needed, enabled only when 2+ files are selected)

#### Paste Text
- Paste any block of text (min 20 characters) and click **Analyze**

#### Quick Sentence Check
- Paste a single sentence in the yellow box and click **Check Sentence**
- Requires corpus documents to be present

#### Empty Corpus Warning
- A yellow banner appears automatically when the corpus is empty
- Directs you to the Corpus tab or suggests using Compare Files

### 📊 Results Tab

- View the **ensemble score** and **risk level** with a visual progress bar
- Inspect **per-document match scores** with cosine and Jaccard breakdown
- Review **flagged sentence pairs** with similarity percentages and source attribution
- For multi-file uploads, click any file card to drill into its full results
- For file-to-file comparisons, click any pair card to expand flagged sentences

### 🗂️ Corpus Tab

#### What to Add to the Corpus

The corpus should contain **reference documents** that represent content you want to check against:

- Academic papers or essays from your institution
- Previously submitted student work (with permission)
- Published articles or textbooks in your subject area
- Any authoritative text relevant to your domain

**Best practices:**
- Add at least **10–20 documents** for reliable detection
- Each document should be **at least 100 words**
- Use **diverse sources** to build a broad vocabulary
- Regularly update the corpus with new submissions

#### Adding Documents
- **Upload File** — add a `.txt`, `.pdf`, or `.docx` as a reference document
- **Paste Text** — manually add content with a custom title

#### Managing Documents
- View word counts and upload dates for all corpus documents
- Remove any document at any time — the index rebuilds automatically

### 🕘 History Tab

- Browse all checks performed in the current session
- Click any entry to reload its full results in the Results tab
- History resets when the server restarts

---

## 🧪 Running Tests

```bash
pytest tests/
```

Tests cover:
- Text preprocessing (stopword removal, lemmatization)
- Shingle creation
- Empty corpus behavior
- Detection with corpus documents
- Add/remove document operations
- Risk level classification

---

## 📦 Dependencies

| Package | Version | Purpose |
|:--|:--|:--|
| `Flask` | ≥3.1.3 | Web framework and routing |
| `scikit-learn` | ≥1.8.0 | TF-IDF vectorization and cosine similarity |
| `datasketch` | ≥1.10.0 | MinHash signatures and LSH indexing |
| `nltk` | ≥3.9.4 | Tokenization, stopword removal, lemmatization |
| `werkzeug` | ≥3.1.8 | Secure filename handling (Flask dependency) |
| `PyPDF2` | ≥3.0.1 | PDF text extraction *(optional)* |
| `python-docx` | ≥1.2.0 | DOCX text extraction *(optional)* |

> NLTK resources (`punkt`, `punkt_tab`, `stopwords`, `wordnet`) are downloaded automatically on first run.

---

## 📝 Notes

- Submission history is stored **in memory only** and resets when the server restarts
- The corpus loads `.txt` files from the `corpus/` directory at startup
- Uploaded PDF and DOCX files are extracted to plain text and saved to the corpus
- For production use, replace in-memory history with a database such as **SQLite** or **PostgreSQL**
- `debug=True` is set in `app.py` — disable this before any public deployment

---

## 🔮 Future Improvements

- [ ] Persistent history storage with a database
- [ ] User authentication and per-user corpus management
- [ ] Semantic similarity via sentence embeddings (`sentence-transformers`)
- [ ] Internet-scale detection via external academic APIs (Google Scholar, Semantic Scholar)
- [ ] Exportable plagiarism reports in PDF format
- [ ] Support for additional file formats (`.odt`, `.rtf`)
- [ ] Incremental TF-IDF updates (avoid full rebuild on every corpus change)
- [ ] Configurable similarity thresholds and weights from the UI
- [ ] OCR support for scanned PDFs

---

<div align="center">

<br/>

Made with dedication by
**Group 6 · Wolkite University**

<br/>

</div>
