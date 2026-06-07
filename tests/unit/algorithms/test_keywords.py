from app.algorithms.keywords import extract_keywords


def test_extracts_relevant_technical_keywords():
    jd = "We need a Python FastAPI backend engineer with PostgreSQL and Docker experience."
    keywords = extract_keywords(jd, top_n=5)
    assert "fastapi" in keywords
    assert "docker" in keywords


def test_empty_text_returns_empty_list():
    assert extract_keywords("") == []
    assert extract_keywords("   ") == []


def test_top_n_limits_result_size():
    jd = "Python Java Go Rust Kotlin Swift TypeScript JavaScript Ruby PHP"
    keywords = extract_keywords(jd, top_n=3)
    assert len(keywords) == 3


def test_filters_short_terms():
    jd = "We use AI ML and Python for data processing"
    keywords = extract_keywords(jd, top_n=10)
    assert all(len(keyword) > 2 for keyword in keywords)
