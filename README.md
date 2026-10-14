# AI Resume Analyzer and Job Recommendation System

An AI/NLP-based educational project that analyzes PDF/DOCX resumes,
extracts job-related skills, recommends suitable roles, identifies skill
gaps and generates a learning roadmap.

## Features

- PDF and DOCX resume upload
- Resume text extraction
- Text cleaning
- Controlled skill extraction
- 7 predefined job roles
- TF-IDF + cosine similarity baseline
- Sentence Transformer semantic matching
- Top 3 job recommendations
- Target-role skill-gap analysis
- Rule-based learning roadmap
- Optional Groq-powered AI feedback
- Interactive Plotly charts
- Downloadable analysis report

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Semantic Matching

The advanced matching mode uses:

```text
all-MiniLM-L6-v2
```

from Sentence Transformers.

The model is downloaded the first time semantic matching is used, so the
first run may take longer and requires internet access.

## Optional Groq AI Feedback

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_api_key_here
```

Then restart Streamlit.

If no key is provided, the rest of the application still works normally.

## Architecture

```text
PDF/DOCX Resume
       |
       v
Text Extraction
       |
       v
Text Cleaning
       |
       v
Skill Extraction
       |
       +--------------------+
       |                    |
       v                    v
Skill Gap             Semantic Matching
                           |
                    Sentence Transformer
                           |
                           v
                    Role Ranking
                           |
             +-------------+-------------+
             |                           |
             v                           v
       Recommendations             Target Role
                                         |
                                         v
                                  Missing Skills
                                         |
                                         v
                                  Learning Roadmap
                                         |
                                         v
                                    AI Feedback
```

## Responsible AI

This system should evaluate only job-related skills, education, projects
and relevant experience. It should not score or infer protected personal
attributes such as gender, age, religion, nationality, marital status,
photograph or disability.

Match scores are estimates, not recruiter decisions.

## Future Improvements

- Job-description upload
- Resume section detection
- Better skill normalization
- RAG-based career guidance
- PDF report generation
- Database and user accounts
- FastAPI backend
- Deployment
