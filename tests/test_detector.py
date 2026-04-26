import pytest
from plagiarism.detector import PlagiarismDetector, preprocess_text, create_shingles


def test_preprocess_text():
    result = preprocess_text("The quick brown foxes are jumping over lazy dogs!")
    assert isinstance(result, str)
    # stopwords like 'the', 'are', 'over' should be removed
    assert 'the' not in result.split()
    assert 'are' not in result.split()


def test_create_shingles():
    shingles = create_shingles("the quick brown fox jumps", k=3)
    assert isinstance(shingles, list)
    assert len(shingles) > 0


def test_check_text_empty_corpus(tmp_path):
    detector = PlagiarismDetector(corpus_dir=tmp_path)
    result = detector.check_text("Hello world, this is a test sentence.")
    assert result["ensemble_score"] == 0.0
    assert result["risk_level"] == "Low"
    assert result["top_matches"] == []
    assert result["flagged_sentences"] == []


def test_check_text_with_corpus(tmp_path):
    doc = tmp_path / "doc1.txt"
    doc.write_text("The quick brown fox jumps over the lazy dog. This is a well known pangram.")

    detector = PlagiarismDetector(corpus_dir=tmp_path)
    result = detector.check_text("The quick brown fox jumps over the lazy dog.")

    assert "ensemble_score" in result
    assert "cosine_score" in result
    assert "jaccard_score" in result
    assert "risk_level" in result
    assert "top_matches" in result
    assert "flagged_sentences" in result
    assert result["ensemble_score"] > 0.0


def test_add_and_remove_document(tmp_path):
    detector = PlagiarismDetector(corpus_dir=tmp_path)
    assert len(detector.documents) == 0

    detector.add_document("Test Doc", "This is a sample reference document for testing purposes.")
    assert len(detector.documents) == 1
    assert detector.documents[0].title == "Test_Doc"

    detector.remove_document("Test_Doc")
    assert len(detector.documents) == 0


def test_risk_levels(tmp_path):
    doc = tmp_path / "ref.txt"
    doc.write_text("Artificial intelligence is transforming the world of technology and science.")

    detector = PlagiarismDetector(corpus_dir=tmp_path)

    result = detector.check_text("Completely unrelated content about cooking recipes and food.")
    assert result["risk_level"] in ["Low", "Moderate", "High", "Critical"]
