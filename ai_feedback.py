import os
from dotenv import load_dotenv

load_dotenv()


def generate_ai_feedback(
    resume_text,
    found_skills,
    target_role,
    match_score,
    missing_skills,
):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return (
            "AI feedback is not configured yet.\n\n"
            "To enable it, create a .env file and add:\n"
            "GROQ_API_KEY=your_api_key_here"
        )

    try:
        from groq import Groq
    except ImportError:
        return "Groq package is not installed. Run: python -m pip install groq"

    client = Groq(api_key=api_key)

    prompt = f"""
You are a career guidance assistant for an educational resume analyzer.

Analyze the resume only for job-related skills, projects, education,
and relevant experience. Do not evaluate or infer protected personal
attributes such as age, gender, religion, nationality, marital status,
disability, or photograph.

Target role: {target_role}
Estimated match score: {match_score}%

Detected skills:
{", ".join(found_skills) if found_skills else "None"}

Missing target-role skills:
{", ".join(missing_skills) if missing_skills else "None"}

Resume text:
{resume_text[:12000]}

Provide:
1. A short overall assessment.
2. Three resume strengths.
3. Three specific improvement suggestions.
4. A practical 4-week learning/project roadmap.
5. One concise project idea that would strengthen the target role.

Do not claim that missing keywords prove the person lacks a skill.
Keep the advice practical for a college student.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You provide responsible, skill-focused career guidance."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1200,
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"AI feedback could not be generated: {error}"
