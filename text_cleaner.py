import re


def clean_text(text):
    text = text.lower()

    # Preserve important technical names during normalization.
    replacements = {
        "c++": "cplusplus",
        "c#": "csharp",
        ".net": "dotnet",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()
