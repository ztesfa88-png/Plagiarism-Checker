<div align="center">

<br/>

---

## 

**College of Computing and Informatics**
**Department of Software Engineering**

*Fundamentals of Software Security*

**SEng7413 · 3rd Year**
Academic Year and Semester: **2018, Semester 2**

<br/>

### 👥 Members

| # | Name | ID |
|:--:|:--|:--|
| 1 | Samir Girle | NSR/0673/16 |
| 2 | Temesgen Teka | NSR/1007/16 |
| 3 | Ysmalem Temesgen | NSR/0843/16 |
| 4 | Yohannes Girma | NSR/0850/16 |
| 5 | Yonas Abera | NSR/0857/16 |
| 6 | Temesgen Demeke | NSR/0765/16 |
| 7 | Zelalem Tesfa | NSR/0868/16 |

<br/>

**Submitted to:** Mr. Belay
**Submission Date:** 30/08/2018

---

<br/>


# Plagiarism Detection System

### An intelligent, ML-powered plagiarism checker built with Flask

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-Enabled-4B8BBE?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

<br/>

> 🎓 Developed by **Group 6 · Wolkite University**

<br/>

</div>

---

## 📌 Overview

The **Plagiarism Detection System** is a web-based application that analyzes submitted text or uploaded documents and compares them against a local corpus of reference documents.

It uses a **hybrid unsupervised machine learning approach** — combining **TF-IDF Cosine Similarity** and **MinHash Jaccard Similarity** — to produce a reliable ensemble plagiarism score with sentence-level match highlighting.

---

## ✨ Features

| Feature | Description |
|:--|:--|
| 📄 **Document Analysis** | Paste full text for document-level plagiarism scanning |
| 🔍 **Sentence Check** | Instantly check a single sentence against the entire corpus |
| 📁 **File Upload** | Upload `.txt`, `.pdf`, or `.docx` files for analysis |
| 🗂️ **Corpus Management** | Add, upload, or remove reference documents via the UI |
| 🧠 **Ensemble Scoring** | Combined TF-IDF + MinHash score for higher accuracy |
| 🚦 **Risk Classification** | Automatic risk level: `Low` / `Moderate` / `High` / `Critical` |
| 📊 **Session History** | Track all checks performed during the current session |

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

## 🌐 API Reference

| Method | Endpoint | Description |
|:--:|:--|:--|
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

## 🚀 Setup and Installation

### Prerequisites

- Python **3.9** or higher
- `pip` package manager

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/plagiarism-checker.git
cd plagiarism-checker
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
pip install -r requirements.txt
```

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
- **Upload File** — Select a `.txt`, `.pdf`, or `.docx` file and click **Upload & Analyze**
- **Paste Text** — Paste any block of text and click **Analyze**
- **Quick Sentence Check** — Paste a single sentence and click **Check Sentence**

### 📊 Results Tab
- View the ensemble score and risk level
- Inspect per-document match scores with cosine and Jaccard breakdown
- Review flagged sentence pairs with similarity percentages and source attribution

### 🗂️ Corpus Tab
- **Upload File** — Add a `.txt`, `.pdf`, or `.docx` directly as a reference document
- **Paste Text** — Manually add a document with a custom title
- View word counts and dates for all corpus documents
- Remove any document from the corpus at any time

### 🕘 History Tab
- Browse all checks performed in the current session
- Click any entry to reload its full results in the Results tab

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📦 Dependencies

| Package | Purpose |
|:--|:--|
| `Flask` | Web framework and routing |
| `scikit-learn` | TF-IDF vectorization and cosine similarity |
| `datasketch` | MinHash signatures and LSH indexing |
| `nltk` | Tokenization, stopword removal, lemmatization |
| `PyPDF2` | PDF text extraction |
| `python-docx` | DOCX text extraction |

> **Note:** NLTK resources (`punkt`, `stopwords`, `wordnet`) are downloaded automatically on first run.

---

## 📝 Notes

- Submission history is stored **in memory only** and resets when the server restarts
- The corpus loads `.txt` files from the `corpus/` directory at startup
- Uploaded PDF and DOCX files are extracted to plain text before being saved to the corpus
- For production use, consider replacing in-memory history with a database such as **SQLite** or **PostgreSQL**

---

## 🔮 Future Improvements

- [ ] Persistent history storage with a database
- [ ] User authentication and per-user corpus management
- [ ] Support for additional file formats (`.odt`, `.rtf`)
- [ ] Internet-scale detection via external academic APIs
- [ ] Exportable plagiarism reports in PDF format

---

<div align="center">

<br/>

Made with ❤️ and dedication by

**Group 6 · Wolkite University**

<br/>

</div>
