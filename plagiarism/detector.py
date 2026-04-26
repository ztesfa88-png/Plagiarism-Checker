import re
import nltk
from pathlib import Path
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datasketch import MinHash, MinHashLSH
import numpy as np

# Download required NLTK data
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass  # Continue even if downloads fail

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize

_WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text: str) -> str:
    """Preprocess text: lowercase, remove punctuation, stopwords, lemmatize."""
    text = text.lower()
    tokens = _WORD_RE.findall(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)


def create_shingles(text: str, k: int = 3) -> list[str]:
    """Create k-shingles from preprocessed text."""
    tokens = preprocess_text(text).split()
    if len(tokens) < k:
        return [' '.join(tokens)]
    return [' '.join(tokens[i:i+k]) for i in range(len(tokens) - k + 1)]


class Document:
    def __init__(self, path: Path, title: str = None):
        self.path = path
        self.title = title or path.stem
        self.raw_text = path.read_text(encoding="utf-8")
        self.preprocessed = preprocess_text(self.raw_text)
        try:
            self.sentences = sent_tokenize(self.raw_text)
        except:
            # Fallback: split by periods if NLTK fails
            self.sentences = [s.strip() for s in self.raw_text.split('.') if s.strip()]
        self.shingles = create_shingles(self.raw_text)
        self.minhash = self._create_minhash()
        self.word_count = len(self.raw_text.split())

    def _create_minhash(self, num_perm: int = 128) -> MinHash:
        """Create MinHash signature for LSH."""
        m = MinHash(num_perm=num_perm)
        for shingle in self.shingles:
            m.update(shingle.encode('utf8'))
        return m


class PlagiarismDetector:
    def __init__(self, corpus_dir: str | Path):
        self.corpus_dir = Path(corpus_dir)
        self.documents = []
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.lsh_index = MinHashLSH(threshold=0.5, num_perm=128)
        self._load_corpus()

    def _load_corpus(self):
        """Load and index corpus documents."""
        if not self.corpus_dir.exists():
            self.corpus_dir.mkdir(parents=True, exist_ok=True)
            return

        self.documents = []
        for path in sorted(self.corpus_dir.glob("*.txt")):
            doc = Document(path)
            self.documents.append(doc)

        self._rebuild_index()

    def _rebuild_index(self):
        """Rebuild the TF-IDF matrix and MinHash index from the current corpus."""
        self.lsh_index = MinHashLSH(threshold=0.5, num_perm=128)
        if not self.documents:
            self.tfidf_vectorizer = None
            self.tfidf_matrix = None
            return

        for doc in self.documents:
            self.lsh_index.insert(doc.title, doc.minhash)

        texts = [doc.preprocessed for doc in self.documents]
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)

    def add_document(self, title: str, text: str):
        """Add a new document to the corpus."""
        filename = f"{title.replace(' ', '_')}.txt"
        path = self.corpus_dir / filename
        path.write_text(text, encoding='utf-8')

        doc = Document(path, title)
        self.documents.append(doc)
        self._rebuild_index()

    def remove_document(self, title: str):
        """Remove a document from the corpus."""
        normalized = title.replace(' ', '_')
        self.documents = [d for d in self.documents if d.title != title and d.path.stem != normalized]

        for path in self.corpus_dir.glob("*.txt"):
            if path.stem == normalized or path.stem == title:
                path.unlink()
                break

        self._rebuild_index()

    def check_text(self, text: str) -> dict:
        """Analyze text for plagiarism."""
        if not self.documents:
            return {
                "cosine_score": 0.0,
                "jaccard_score": 0.0,
                "ensemble_score": 0.0,
                "risk_level": "Low",
                "top_matches": [],
                "flagged_sentences": [],
                "preprocessed_tokens": len(preprocess_text(text).split()),
                "shingles_count": len(create_shingles(text)),
                "explanation": "No documents in corpus. The analysis shows no plagiarism as there are no reference documents to compare against."
            }

        # Preprocess input
        preprocessed_input = preprocess_text(text)
        try:
            input_sentences = sent_tokenize(text)
        except:
            input_sentences = [s.strip() for s in text.split('.') if s.strip()]
        input_shingles = create_shingles(text)

        # Create MinHash for input
        input_minhash = MinHash(num_perm=128)
        for shingle in input_shingles:
            input_minhash.update(shingle.encode('utf8'))

        # Find LSH candidates
        candidates = self.lsh_index.query(input_minhash)
        if not candidates:
            candidates = [doc.title for doc in self.documents[:5]]  # Fallback to top 5

        # Calculate similarities
        cosine_scores = {}
        jaccard_scores = {}

        input_tfidf = self.tfidf_vectorizer.transform([preprocessed_input])

        for doc in self.documents:
            if doc.title in candidates:
                # Cosine similarity
                doc_idx = self.documents.index(doc)
                cosine_sim = cosine_similarity(input_tfidf, self.tfidf_matrix[doc_idx:doc_idx+1])[0][0]
                cosine_scores[doc.title] = cosine_sim

                # Jaccard similarity (from MinHash)
                jaccard_sim = input_minhash.jaccard(doc.minhash)
                jaccard_scores[doc.title] = jaccard_sim

        # Get top matches
        top_matches = []
        for title in candidates[:5]:
            if title in cosine_scores:
                score = 0.6 * cosine_scores[title] + 0.4 * jaccard_scores[title]
                top_matches.append({
                    "doc_id": title,
                    "title": title,
                    "score": round(score, 3),
                    "note": f"Cosine: {cosine_scores[title]:.2f}, Jaccard: {jaccard_scores[title]:.2f}"
                })

        top_matches.sort(key=lambda x: x["score"], reverse=True)

        # Calculate overall scores
        if top_matches:
            max_cosine = max(cosine_scores.values())
            max_jaccard = max(jaccard_scores.values())
            ensemble_score = 0.6 * max_cosine + 0.4 * max_jaccard
        else:
            max_cosine = max_jaccard = ensemble_score = 0.0

        # Determine risk level
        if ensemble_score >= 0.76:
            risk_level = "Critical"
        elif ensemble_score >= 0.51:
            risk_level = "High"
        elif ensemble_score >= 0.26:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        # Flag sentences with high similarity
        flagged_sentences = []
        for input_sent in input_sentences:
            input_sent_preprocessed = preprocess_text(input_sent)
            if len(input_sent_preprocessed.split()) < 3:
                continue

            input_sent_tfidf = self.tfidf_vectorizer.transform([input_sent_preprocessed])

            for doc in self.documents:
                for doc_sent in doc.sentences:
                    doc_sent_preprocessed = preprocess_text(doc_sent)
                    if len(doc_sent_preprocessed.split()) < 3:
                        continue

                    doc_sent_tfidf = self.tfidf_vectorizer.transform([doc_sent_preprocessed])
                    sim = cosine_similarity(input_sent_tfidf, doc_sent_tfidf)[0][0]

                    if sim >= 0.70:
                        flagged_sentences.append({
                            "submitted": input_sent.strip(),
                            "matched": doc_sent.strip(),
                            "source": doc.title,
                            "similarity": round(sim, 3)
                        })
                        break  # Only flag once per input sentence

        # Explanation
        if ensemble_score == 0:
            explanation = "The submitted text shows no significant similarity to any documents in the corpus. This suggests the content is original."
        elif risk_level == "Low":
            explanation = f"The text shows minimal similarity ({ensemble_score:.1%}) to corpus documents, indicating mostly original content with minor overlaps."
        elif risk_level == "Moderate":
            explanation = f"The text shows moderate similarity ({ensemble_score:.1%}) to corpus documents. Some sections may need review for potential plagiarism."
        elif risk_level == "High":
            explanation = f"The text shows high similarity ({ensemble_score:.1%}) to corpus documents. Multiple sections appear to be copied or closely paraphrased."
        else:
            explanation = f"The text shows critical similarity ({ensemble_score:.1%}) to corpus documents. Most content appears to be plagiarized."

        return {
            "cosine_score": round(max_cosine, 3),
            "jaccard_score": round(max_jaccard, 3),
            "ensemble_score": round(ensemble_score, 3),
            "risk_level": risk_level,
            "top_matches": top_matches,
            "flagged_sentences": flagged_sentences,
            "preprocessed_tokens": len(preprocessed_input.split()),
            "shingles_count": len(input_shingles),
            "explanation": explanation
        }
