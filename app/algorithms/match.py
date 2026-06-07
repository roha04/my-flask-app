from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_resume_to_jd(resume_text: str, jd_text: str) -> float:
    """Return cosine similarity [0, 1] between resume and job description."""
    resume = resume_text.strip()
    jd = jd_text.strip()
    if not resume or not jd:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([resume, jd])
    score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    return max(0.0, min(1.0, score))
