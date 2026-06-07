from sklearn.feature_extraction.text import TfidfVectorizer


def extract_keywords(jd_text: str, top_n: int = 10) -> list[str]:
    """Extract top-N keywords from a job description using TF-IDF term scores."""
    text = jd_text.strip()
    if not text or top_n <= 0:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z+\.#]{1,}\b",
    )
    matrix = vectorizer.fit_transform([text])
    scores = matrix.toarray()[0]
    terms = vectorizer.get_feature_names_out()

    ranked = sorted(zip(terms, scores, strict=True), key=lambda item: item[1], reverse=True)
    keywords: list[str] = []
    for term, score in ranked:
        if score <= 0 or len(term) <= 2:
            continue
        keywords.append(term)
        if len(keywords) >= top_n:
            break
    return keywords
