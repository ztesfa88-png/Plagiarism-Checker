# Plagiarism Checker

A Flask-based plagiarism detection application that compares submitted text and uploaded files against a local corpus of documents.

## What this project does

- Accepts text input from the web interface or uploaded `.txt`, `.pdf`, and `.docx` files.
- Compares the submitted content against a local corpus of documents stored in `corpus/`.
- Calculates similarity using a hybrid algorithm of TF-IDF cosine similarity and MinHash Jaccard similarity.
- Highlights sentence-level matches and assigns a risk level (Low / Moderate / High / Critical).
- Supports adding and removing corpus documents via API.
- Tracks recent history in memory during runtime.

## How it works

The application consists of a Flask backend, a detection engine, and a responsive frontend.

### Backend (`app.py`)

- Initializes Flask and configures file upload handling.
- Loads the plagiarism detector from `plagiarism/detector.py` using the `corpus/` folder.
- Exposes routes:
  - `/` : serves the HTML interface.
  - `/check` : checks pasted text for plagiarism.
  - `/check_sentence` : checks a single sentence against the corpus.
  - `/upload` : uploads a file and checks its text.
  - `/corpus` : lists, adds, or deletes corpus documents.

### Detection engine (`plagiarism/detector.py`)

- Reads `.txt` corpus documents from `corpus/`.
- Preprocesses text by lowercasing, tokenizing, removing stopwords, and lemmatizing.
- Builds a TF-IDF matrix for cosine similarity.
- Builds a MinHash LSH index for fast approximate Jaccard similarity.
- Performs sentence-level analysis to flag highly similar sentence pairs.

### Frontend

- The HTML interface allows the user to:
  - Paste text for document-level plagiarism scanning.
  - Paste a single sentence for sentence-level checking.
  - Upload a file to scan its contents.
  - View recent check history and corpus document status.

## Detailed code explanation

### `app.py`

#### Configuration

- `UPLOAD_FOLDER`: where uploaded files are temporarily saved.
- `ALLOWED_EXTENSIONS`: supported upload types.
- `MAX_CONTENT_LENGTH`: limits file uploads to 16 MB.

#### `allowed_file(filename)`

Checks whether the uploaded file extension is allowed.

#### `extract_text_from_file(filepath)`

Reads text from uploaded files:
- `.txt` files are read directly.
- `.pdf` uses `PyPDF2` if installed.
- `.docx` uses `python-docx` if installed.

Returns an error message string if the required dependency is missing.

#### `/upload`

Receives file uploads from the browser, extracts text, runs the plagiarism check, and returns JSON results.

#### `/check`

Receives raw text from the frontend, validates size, and sends the text to `detector.check_text()`.

#### `/check_sentence`

Receives a single sentence and compares it against each sentence in every corpus document using TF-IDF cosine similarity.

- Uses a lower threshold (`>= 0.3`) because sentences are shorter than full documents.
- Collects the top sentence matches and returns match details.
- Computes a risk level based on the best sentence similarity.

#### `/corpus`

Provides corpus management:
- `GET` returns current corpus documents.
- `POST` adds a new document by saving it to `corpus/` and rebuilding the detector.
- `DELETE` removes a document and updates the corpus index.

### `plagiarism/detector.py`

#### Text preprocessing helpers

- `preprocess_text(text)`:
  - Converts text to lowercase.
  - Extracts word tokens.
  - Removes stopwords.
  - Lemmatizes each token.
  - Returns normalized text suitable for feature extraction.

- `create_shingles(text, k=3)`:
  - Builds overlapping token windows of length `k`.
  - Shingles are used for MinHash similarity.

#### `Document`

Represents one corpus document:
- Loads raw text from disk.
- Stores preprocessed text.
- Splits text into sentences using NLTK, with a fallback split on periods.
- Creates shingles and a MinHash signature.
- Stores word count for metadata.

#### `PlagiarismDetector`

Main detection engine:
- Loads corpus documents and builds TF-IDF and MinHash indexes.
- `add_document()` saves a new corpus file and updates the indexes.
- `remove_document()` deletes a file and rebuilds indexes.

##### `check_text(text)`

Analyzes input text and returns a detailed JSON result.

Steps:
1. Preprocesses user text.
2. Builds shingles and a MinHash signature for the input.
3. Queries the MinHash LSH index to find candidate corpus documents.
4. Computes TF-IDF cosine similarity for each candidate document.
5. Computes MinHash Jaccard similarity for each candidate.
6. Calculates an ensemble score:
   - `ensemble = 0.6 * cosine + 0.4 * jaccard`
7. Defines a risk level based on ensemble score.
8. Performs sentence-level matching by comparing each input sentence against corpus sentences using TF-IDF similarity.
9. Builds an explanation string and returns:
   - `cosine_score`, `jaccard_score`, `ensemble_score`
   - `risk_level`
   - `top_matches`
   - `flagged_sentences`
   - `preprocessed_tokens`, `shingles_count`
   - `explanation`

## Project structure

- `app.py`: Flask app, routing, file upload and history handling.
- `plagiarism/detector.py`: core plagiarism logic and document indexing.
- `templates/index.html`: user interface.
- `static/style.css`: UI styling and layout.
- `corpus/`: local reference documents used for similarity checks.
- `tests/`: unit tests for the detection engine.

## Setup and run

1. Create a Python virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the application:

```powershell
python app.py
```

4. Open the app in your browser:

```powershell
http://127.0.0.1:5000
```

## Usage

- Paste a full text block, then click **Check Text**.
- Paste a sentence, then click **Check Sentence**.
- Upload `.txt`, `.pdf`, or `.docx` files using the upload section.
- Manage corpus files via the corpus API or by adding new `.txt` files into `corpus/`.

## Notes

- The history data is stored in memory for the current session only.
- PDF and DOCX support require optional packages: `PyPDF2` and `python-docx`.
- NLTK resources are downloaded at runtime if missing.

## Extending the project

Suggestions for future improvements:
- Store history in a database instead of memory.
- Add support for more file formats.
- Improve sentence tokenization and matching thresholds.
- Add user authentication and project-specific corpora.
