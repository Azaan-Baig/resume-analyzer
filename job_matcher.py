from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


DATA_FILE = Path(__file__).parent / "data" / "job_roles.csv"
MODEL_NAME = "all-MiniLM-L6-v2"


def load_job_roles():
    return pd.read_csv(DATA_FILE)


def calculate_tfidf_scores(resume_text):
    jobs = load_job_roles()
    documents = [resume_text] + jobs["skills"].fillna("").tolist()

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)
    scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    return [
        {
            "role": jobs.iloc[i]["role"],
            "score": round(float(score) * 100, 2),
        }
        for i, score in enumerate(scores)
    ]


def calculate_semantic_scores(resume_text):
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        return None

    jobs = load_job_roles()
    job_documents = jobs["skills"].fillna("").tolist()

    model = SentenceTransformer(MODEL_NAME)

    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True
    )

    job_embeddings = model.encode(
        job_documents,
        normalize_embeddings=True
    )

    scores = cosine_similarity(
        resume_embedding,
        job_embeddings
    ).flatten()

    # Map cosine similarity roughly to a 0-100 display score.
    # It is still an estimate, not a probability.
    display_scores = [
        max(0.0, min(100.0, float(score) * 100))
        for score in scores
    ]

    return [
        {
            "role": jobs.iloc[i]["role"],
            "score": round(display_scores[i], 2),
        }
        for i in range(len(scores))
    ]


def calculate_match_scores(resume_text, method="semantic"):
    if method == "semantic":
        results = calculate_semantic_scores(resume_text)
        if results is not None:
            return sorted(
                results,
                key=lambda x: x["score"],
                reverse=True
            )

    results = calculate_tfidf_scores(resume_text)

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )


def get_skill_gap(found_skills, role):
    jobs = load_job_roles()
    job = jobs[jobs["role"] == role]

    if job.empty:
        return [], []

    required = [
        skill.strip()
        for skill in job.iloc[0]["skills"].split(",")
        if skill.strip()
    ]

    found_lookup = {skill.lower(): skill for skill in found_skills}

    matched = []
    missing = []

    for skill in required:
        if skill.lower() in found_lookup:
            matched.append(found_lookup[skill.lower()])
        else:
            missing.append(skill)

    return matched, missing
