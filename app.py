from flask import Flask, render_template, request, jsonify
from plagiarism.detector import PlagiarismDetector, preprocess_text, create_shingles
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

detector = PlagiarismDetector(corpus_dir="corpus")

# In-memory storage for history (in production, use database)
history = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath):
    """Extract text from uploaded file"""
    try:
        file_ext = filepath.rsplit('.', 1)[1].lower()
        
        if file_ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_ext == 'pdf':
            try:
                import PyPDF2
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    return text
            except ImportError:
                return "PDF support requires PyPDF2. Install with: pip install PyPDF2"
        
        elif file_ext == 'docx':
            try:
                from docx import Document
                doc = Document(filepath)
                return "\n".join([paragraph.text for paragraph in doc.paragraphs])
            except ImportError:
                return "DOCX support requires python-docx. Install with: pip install python-docx"
    
    except Exception as e:
        return f"Error extracting text: {str(e)}"

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload and plagiarism check"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Only .txt, .pdf, and .docx files allowed"}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        text = extract_text_from_file(filepath)
        
        if not text or len(text) < 20:
            return jsonify({"error": "File is empty or too small"}), 400
        
        # Run plagiarism check
        result = detector.check_text(text)
        
        # Add to history with file info
        history_entry = {
            **result,
            "filename": filename,
            "text": text[:120] + "..." if len(text) > 120 else text,
            "timestamp": datetime.now().isoformat()
        }
        history.insert(0, history_entry)

        if len(history) > 50:
            history.pop()

        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text or len(text) < 20:
        return jsonify({"error": "Please enter at least a sentence of text to analyze."}), 400

    result = detector.check_text(text)

    # Add to history
    history_entry = {
        **result,
        "text": text[:120] + "..." if len(text) > 120 else text,
        "timestamp": datetime.now().isoformat()
    }
    history.insert(0, history_entry)

    # Keep only last 50 entries
    if len(history) > 50:
        history.pop()

    return jsonify(result)

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(history)

@app.route("/corpus/upload", methods=["POST"])
def corpus_upload():
    """Upload a file directly into the corpus."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only .txt, .pdf, and .docx files allowed"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text_from_file(filepath)

        try:
            os.remove(filepath)
        except:
            pass

        if not text or len(text) < 20:
            return jsonify({"error": "File is empty or too small to add to corpus"}), 400

        title = os.path.splitext(filename)[0]
        detector.add_document(title, text)
        return jsonify({"message": f'"{title}" added to corpus successfully.'})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/corpus", methods=["GET", "POST", "DELETE"])
def corpus():
    if request.method == "GET":
        corpus_docs = []
        for doc in detector.documents:
            corpus_docs.append({
                "title": doc.title,
                "word_count": doc.word_count,
                "added_at": datetime.fromtimestamp(doc.path.stat().st_mtime).isoformat()
            })
        return jsonify(corpus_docs)

    elif request.method == "POST":
        data = request.get_json()
        title = data.get("title", "").strip()
        text = data.get("text", "").strip()

        if not title or not text or len(text) < 20:
            return jsonify({"error": "Please provide a title and document text."}), 400

        try:
            detector.add_document(title, text)
            return jsonify({"message": "Document added to corpus successfully."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "DELETE":
        data = request.get_json()
        title = data.get("title", "").strip()

        if not title:
            return jsonify({"error": "Please provide a document title to remove."}), 400

        try:
            detector.remove_document(title)
            return jsonify({"message": "Document removed from corpus successfully."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/check_sentence", methods=["POST"])
def check_sentence():
    """Check a single sentence against corpus"""
    data = request.get_json()
    sentence = data.get("sentence", "").strip()

    if not sentence or len(sentence) < 10:
        return jsonify({"error": "Please enter at least a sentence to analyze."}), 400

    # Find matches for this sentence
    matches = []
    for doc in detector.documents:
        # Check sentence similarity
        for doc_sent in doc.sentences:
            try:
                # Simple text similarity check
                sent1 = preprocess_text(sentence)
                sent2 = preprocess_text(doc_sent)
                
                if len(sent1.split()) < 2 or len(sent2.split()) < 2:
                    continue
                
                # TF-IDF similarity
                input_tfidf = detector.tfidf_vectorizer.transform([sent1])
                doc_sent_tfidf = detector.tfidf_vectorizer.transform([sent2])
                similarity = cosine_similarity(input_tfidf, doc_sent_tfidf)[0][0]
                
                if similarity >= 0.3:  # Lower threshold for sentence checking
                    matches.append({
                        "submitted": sentence,
                        "matched": doc_sent.strip(),
                        "source": doc.title,
                        "similarity": round(similarity, 3),
                        "file_match": True
                    })
            except:
                continue
    
    # Sort by similarity
    matches.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Take top 10 matches
    matches = matches[:10]
    
    # Calculate overall score
    if matches:
        max_similarity = max(m["similarity"] for m in matches)
        if max_similarity >= 0.8:
            risk_level = "Critical"
        elif max_similarity >= 0.6:
            risk_level = "High"
        elif max_similarity >= 0.4:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
    else:
        max_similarity = 0.0
        risk_level = "Low"
    
    result = {
        "cosine_score": round(max_similarity, 3),
        "jaccard_score": round(max_similarity, 3),  # Simplified for sentence check
        "ensemble_score": round(max_similarity, 3),
        "risk_level": risk_level,
        "top_matches": [],
        "flagged_sentences": matches,
        "preprocessed_tokens": len(preprocess_text(sentence).split()),
        "shingles_count": len(create_shingles(sentence)),
        "explanation": f"Sentence checked against {len(detector.documents)} corpus documents. Found {len(matches)} similar sentences."
    }
    
    # Add to history
    history_entry = {
        **result,
        "text": sentence,
        "timestamp": datetime.now().isoformat(),
        "type": "sentence_check"
    }
    history.insert(0, history_entry)

    if len(history) > 50:
        history.pop()

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
