from pathlib import Path
import pandas as pd


DATA_FILE = Path(__file__).parent / "data" / "skill_dictionary.csv"


def load_skills():
    df = pd.read_csv(DATA_FILE)
    return dict(zip(df["skill"], df["category"]))


def extract_skills(text):
    skills = load_skills()
    text_lower = text.lower()

    found = []

    for skill in skills:
        if skill.lower() in text_lower:
            found.append(skill)

    return sorted(found)


def get_skill_categories(found_skills):
    skills = load_skills()
    categories = {}

    for skill in found_skills:
        category = skills.get(skill, "Other")
        categories.setdefault(category, []).append(skill)

    return categories
