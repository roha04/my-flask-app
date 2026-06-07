from app.algorithms.match import match_resume_to_jd


def test_identical_texts_have_high_score():
    text = "Python FastAPI SQLAlchemy developer with REST API experience"
    score = match_resume_to_jd(text, text)
    assert score >= 0.99


def test_unrelated_texts_have_low_score():
    resume = "Chef specializing in Italian pasta and kitchen management"
    jd = "Senior Python backend engineer with FastAPI and PostgreSQL"
    score = match_resume_to_jd(resume, jd)
    assert score < 0.2


def test_empty_input_returns_zero():
    assert match_resume_to_jd("", "Python developer") == 0.0
    assert match_resume_to_jd("Python developer", "") == 0.0


def test_partial_overlap_is_between_extremes():
    resume = "Python developer with Django experience"
    jd = "Python developer with FastAPI and PostgreSQL experience"
    score = match_resume_to_jd(resume, jd)
    assert 0.1 < score < 0.9
