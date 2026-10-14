import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills, get_skill_categories
from job_matcher import (
    calculate_match_scores,
    get_skill_gap,
    SENTENCE_TRANSFORMERS_AVAILABLE,
)
from roadmap_generator import generate_roadmap
from ai_feedback import generate_ai_feedback


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 25px;
    }
    .stApp{
    background-color: aliceblue;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Semantic resume matching • Skill gaps • Job recommendations • AI feedback</div>',
    unsafe_allow_html=True,
)

st.info(
    "This is an educational career-guidance system. Match scores are estimates "
    "and should not be treated as hiring or rejection decisions."
)

with st.sidebar:
    st.header("⚙️ Matching Settings")

    if SENTENCE_TRANSFORMERS_AVAILABLE:
        method = st.radio(
            "Matching method",
            ["Semantic (Sentence Transformer)", "TF-IDF"],
            index=0,
        )
    else:
        method = "TF-IDF"
        st.warning(
            "Sentence Transformers is unavailable. Using TF-IDF."
        )

    st.divider()

    st.header("About")
    st.write(
        "The semantic mode uses the all-MiniLM-L6-v2 Sentence Transformer "
        "to compare the meaning of the resume with role requirements."
    )

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"],
)

if uploaded_file is None:
    st.markdown("### 👆 Upload a PDF or DOCX resume to begin")
    st.stop()

st.success(f"Uploaded: **{uploaded_file.name}**")

try:
    resume_text = extract_resume_text(uploaded_file)

    if not resume_text.strip():
        st.error(
            "No readable text was found. This may be a scanned/image-only PDF."
        )
        st.stop()

    cleaned_text = clean_text(resume_text)

    found_skills = extract_skills(cleaned_text)
    categories = get_skill_categories(found_skills)

    st.header("📊 Resume Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Skills Detected", len(found_skills))
    c2.metric("Characters Extracted", len(resume_text))
    c3.metric("Roles Compared", 7)

    st.header("🛠️ Skills Found")

    if found_skills:
        cols = st.columns(4)
        for index, skill in enumerate(found_skills):
            cols[index % 4].success(skill)
    else:
        st.warning("No skills from the current dictionary were detected.")

    if categories:
        st.subheader("Skills by Category")

        category_df = pd.DataFrame([
            {"Category": category, "Skills": len(skills)}
            for category, skills in categories.items()
        ])

        fig = px.bar(
            category_df,
            x="Category",
            y="Skills",
            title="Detected Skills by Category",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.header("🎯 Job Role Recommendations")

    matching_method = (
        "semantic"
        if method.startswith("Semantic")
        else "tfidf"
    )

    with st.spinner("Comparing your resume with job roles..."):
        match_results = calculate_match_scores(
            cleaned_text,
            method=matching_method,
        )

    result_df = pd.DataFrame(match_results)

    if matching_method == "semantic":
        st.caption(
            "Semantic matching compares the meaning of resume text and role "
            "requirements using Sentence Transformers."
        )
    else:
        st.caption(
            "TF-IDF matching compares important terms between the resume "
            "and role requirements."
        )

    st.subheader("🏆 Top 3 Recommended Roles")

    for position, (_, row) in enumerate(
        result_df.head(3).iterrows(),
        start=1,
    ):
        st.subheader(f"{position}. {row['role']}")
        st.progress(
            min(max(int(round(row["score"])), 0), 100)
        )
        st.write(f"**Estimated Match Score: {row['score']}%**")

    st.subheader("All Role Scores")

    chart_df = result_df.sort_values("score", ascending=True)

    fig = px.bar(
        chart_df,
        x="score",
        y="role",
        orientation="h",
        text="score",
        title="Resume-to-Role Match",
    )

    fig.update_layout(
        xaxis_title="Estimated Match Score (%)",
        yaxis_title="Job Role",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("🎯 Target Role Analysis")

    selected_role = st.selectbox(
        "Select a target role",
        result_df["role"].tolist(),
    )

    selected_score = float(
        result_df.loc[
            result_df["role"] == selected_role,
            "score",
        ].iloc[0]
    )

    st.metric(
        "Estimated Match Score",
        f"{selected_score}%",
    )

    matched, missing = get_skill_gap(
        found_skills,
        selected_role,
    )

    left, right = st.columns(2)

    with left:
        st.subheader("✅ Skills Found")

        if matched:
            for skill in matched:
                st.success(skill)
        else:
            st.write("No required skills detected.")

    with right:
        st.subheader("❌ Missing Skills")

        if missing:
            for skill in missing:
                st.error(skill)
        else:
            st.success("No major missing skills!")

    st.header("📚 Rule-Based Learning Roadmap")

    roadmap = generate_roadmap(missing)

    if roadmap:
        for index, topic in enumerate(roadmap, start=1):
            st.write(f"**Step {index}:** {topic}")
    else:
        st.success(
            "Your detected skills cover the required skills for this role."
        )

    st.header("🤖 AI Resume Feedback")

    if st.button("Generate AI Feedback", type="primary"):
        with st.spinner("Generating AI feedback..."):
            feedback = generate_ai_feedback(
                resume_text=resume_text,
                found_skills=found_skills,
                target_role=selected_role,
                match_score=selected_score,
                missing_skills=missing,
            )

        st.markdown(feedback)

    st.header("📥 Download Analysis")

    report = [
        "AI RESUME ANALYZER REPORT",
        "=" * 40,
        f"Resume: {uploaded_file.name}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Matching Method: {method}",
        "",
        "SKILLS FOUND",
        "-" * 20,
    ]

    report.extend(f"- {skill}" for skill in found_skills)

    report.extend([
        "",
        "JOB ROLE MATCHES",
        "-" * 20,
    ])

    report.extend(
        f"- {row['role']}: {row['score']}%"
        for _, row in result_df.iterrows()
    )

    report.extend([
        "",
        f"TARGET ROLE: {selected_role}",
        f"MATCH SCORE: {selected_score}%",
        "",
        "MATCHED SKILLS",
        "-" * 20,
    ])

    report.extend(f"- {skill}" for skill in matched)

    report.extend([
        "",
        "MISSING SKILLS",
        "-" * 20,
    ])

    report.extend(f"- {skill}" for skill in missing)

    report.extend([
        "",
        "LEARNING ROADMAP",
        "-" * 20,
    ])

    report.extend(
        f"{i}. {topic}"
        for i, topic in enumerate(roadmap, 1)
    )

    st.download_button(
        "⬇️ Download Analysis Report",
        data="\n".join(report),
        file_name="resume_analysis_report.txt",
        mime="text/plain",
    )

    with st.expander("🔎 View Extracted Resume Text"):
        st.text_area(
            "Extracted text",
            resume_text,
            height=350,
        )

except Exception as error:
    st.error(f"An error occurred: {error}")
    st.exception(error)
