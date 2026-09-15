import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .score-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background-color: #f5f7fb;
        border: 1px solid #dddddd;
    }

    .score-number {
        font-size: 42px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">📄 AI-Based Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Resume Analysis + LangChain AI + Fuzzy Logic Job Suitability Prediction
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("⚙️ Settings")

    st.markdown("### 🔑 Gemini API Key")

    # Try to read API key from Streamlit secrets
    try:
        default_api_key = st.secrets.get(
            "GOOGLE_API_KEY",
            ""
        )
    except Exception:
        default_api_key = ""

    api_key = st.text_input(
        "Enter Gemini API Key",
        value=default_api_key,
        type="password",
        help="Your API key is used only for Gemini analysis."
    )

    st.markdown("---")

    st.markdown(
        """
        ### 🧠 AI Component

        **LangChain + Gemini**

        Used for:
        - Resume understanding
        - Job description understanding
        - Information extraction
        - AI explanation
        """
    )

    st.markdown("---")

    st.markdown(
        """
        ### 🌫️ Fuzzy Logic

        Inputs:

        - Skill Match
        - Experience Match
        - Education Match
        - Project Match

        Output:

        **Job Suitability Score**
        """
    )


# ==========================================================
# INPUT SECTION
# ==========================================================

st.header("1️⃣ Upload Resume")

resume_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX and TXT"
)


st.header("2️⃣ Enter Job Description")

job_description = st.text_area(
    "Paste the Job Description",
    height=250,
    placeholder=(
        "Example:\n"
        "We are looking for a Full Stack Developer "
        "with skills in Python, JavaScript, React, "
        "HTML, CSS and MySQL."
    )
)


# ==========================================================
# ANALYZE BUTTON
# ==========================================================

analyze_button = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)


# ==========================================================
# ANALYSIS
# ==========================================================

if analyze_button:

    # ------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------

    if not api_key:
        st.error(
            "❌ Please enter your Google Gemini API key "
            "in the sidebar."
        )
        st.stop()

    if resume_file is None:
        st.error(
            "❌ Please upload your resume."
        )
        st.stop()

    if not job_description.strip():
        st.error(
            "❌ Please enter the job description."
        )
        st.stop()


    # ------------------------------------------------------
    # IMPORT PROJECT MODULES
    # ------------------------------------------------------

    try:

        from resume_parser import extract_resume_text

        from llm_chain import (
            analyze_resume,
            analyze_job_description,
            generate_explanation
        )

        from matcher import calculate_all_scores

        from fuzzy_logic import (
            get_category,
            get_fuzzy_analysis
        )

    except Exception as e:

        st.error(
            "❌ Error loading project modules."
        )

        st.exception(e)

        st.stop()


    # ------------------------------------------------------
    # STEP 1: EXTRACT RESUME TEXT
    # ------------------------------------------------------

    st.subheader("📄 Resume Processing")

    with st.spinner(
        "Extracting text from resume..."
    ):

        try:

            resume_text = extract_resume_text(
                resume_file
            )

            if not resume_text.strip():

                st.error(
                    "❌ No text could be extracted "
                    "from the uploaded resume."
                )

                st.stop()

            st.success(
                "✅ Resume text extracted successfully."
            )

        except Exception as e:

            st.error(
                "❌ Error while extracting resume."
            )

            st.exception(e)

            st.stop()


    # ------------------------------------------------------
    # SHOW EXTRACTED TEXT
    # ------------------------------------------------------

    with st.expander(
        "📃 View Extracted Resume Text"
    ):

        st.text(
            resume_text
        )


    # ------------------------------------------------------
    # STEP 2: LANGCHAIN RESUME ANALYSIS
    # ------------------------------------------------------

    st.subheader(
        "🤖 AI Resume Analysis"
    )

    with st.spinner(
        "Gemini is analyzing the resume..."
    ):

        try:

            candidate_info = analyze_resume(
                resume_text,
                api_key
            )

        except Exception as e:

            st.error(
                "❌ Error occurred while analyzing the resume."
            )

            st.exception(e)

            st.stop()


    with st.expander(
        "👤 View AI Candidate Analysis",
        expanded=True
    ):

        st.write(
            candidate_info
        )


    # ------------------------------------------------------
    # STEP 3: LANGCHAIN JOB ANALYSIS
    # ------------------------------------------------------

    with st.spinner(
        "Gemini is analyzing the job description..."
    ):

        try:

            job_info = analyze_job_description(
                job_description,
                api_key
            )

        except Exception as e:

            st.error(
                "❌ Error occurred while analyzing "
                "the job description."
            )

            st.exception(e)

            st.stop()


    with st.expander(
        "💼 View AI Job Analysis",
        expanded=True
    ):

        st.write(
            job_info
        )


    # ------------------------------------------------------
    # STEP 4: MATCHING
    # ------------------------------------------------------

    st.subheader(
        "📊 Resume-Job Matching"
    )

    with st.spinner(
        "Calculating resume-job matching scores..."
    ):

        try:

            results = calculate_all_scores(
                candidate_info,
                job_info
            )

        except Exception as e:

            st.error(
                "❌ Error occurred while calculating "
                "matching scores."
            )

            st.exception(e)

            st.stop()


    skill_score = float(
        results["skill_match"]
    )

    experience_score = float(
        results["experience_match"]
    )

    education_score = float(
        results["education_match"]
    )

    project_score = float(
        results["project_match"]
    )

    final_score = float(
        results["final_score"]
    )


    # ------------------------------------------------------
    # CATEGORY
    # ------------------------------------------------------

    category = get_category(
        final_score
    )


    # ======================================================
    # SCORE CARDS
    # ======================================================

    st.markdown(
        "### 📈 Matching Scores"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Skill Match",
            f"{skill_score:.2f}%"
        )

    with col2:

        st.metric(
            "Experience Match",
            f"{experience_score:.2f}%"
        )

    with col3:

        st.metric(
            "Education Match",
            f"{education_score:.2f}%"
        )

    with col4:

        st.metric(
            "Project Match",
            f"{project_score:.2f}%"
        )


    # ======================================================
    # FUZZY LOGIC
    # ======================================================

    st.subheader(
        "🌫️ Fuzzy Logic Job Suitability"
    )

    st.info(
        """
        The four matching scores are given to the
        fuzzy inference system.

        The fuzzy system performs:

        **Fuzzification → Rule Evaluation → Aggregation → Defuzzification**
        """
    )


    # ------------------------------------------------------
    # FINAL SCORE
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="score-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### Final Suitability"
        )

        st.markdown(
            f'<div class="score-number">{final_score:.2f}/100</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"### {category}"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with col2:

        st.progress(
            int(
                max(
                    0,
                    min(
                        100,
                        final_score
                    )
                )
            )
        )

        st.write(
            f"**Suitability Score:** "
            f"{final_score:.2f}%"
        )

        st.write(
            f"**Category:** {category}"
        )


    # ======================================================
    # CHART
    # ======================================================

    st.subheader(
        "📊 Match Score Comparison"
    )

    chart_data = pd.DataFrame(
        {
            "Parameter": [
                "Skill Match",
                "Experience Match",
                "Education Match",
                "Project Match"
            ],

            "Score": [
                skill_score,
                experience_score,
                education_score,
                project_score
            ]
        }
    )


    fig = px.bar(
        chart_data,
        x="Parameter",
        y="Score",
        range_y=[0, 100],
        text="Score",
        title="Resume vs Job Requirement"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ======================================================
    # FUZZY MEMBERSHIP VALUES
    # ======================================================

    st.subheader(
        "🔬 Fuzzy Membership Analysis"
    )

    try:

        fuzzy_analysis = get_fuzzy_analysis(
            skill_score,
            experience_score,
            education_score,
            project_score,
            final_score
        )


        membership_rows = []

        for parameter in [
            "Skill Match",
            "Experience Match",
            "Education Match",
            "Project Match"
        ]:

            values = fuzzy_analysis[
                parameter
            ]

            membership_rows.append(
                {
                    "Parameter": parameter,
                    "Low": values["Low"],
                    "Medium": values["Medium"],
                    "High": values["High"]
                }
            )


        membership_df = pd.DataFrame(
            membership_rows
        )


        st.dataframe(
            membership_df,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.warning(
            "Could not display membership analysis."
        )

        st.exception(e)


    # ======================================================
    # AI EXPLANATION
    # ======================================================

    st.subheader(
        "🧠 AI Career Advisor"
    )

    with st.spinner(
        "Generating AI explanation..."
    ):

        try:

            explanation = generate_explanation(
                skill_score,
                experience_score,
                education_score,
                project_score,
                final_score,
                category,
                candidate_info,
                job_info,
                api_key
            )

            st.success(
                "✅ AI explanation generated successfully."
            )

            st.markdown(
                explanation
            )

        except Exception as e:

            st.error(
                "❌ Error generating AI explanation."
            )

            st.exception(e)


    # ======================================================
    # FINAL SUMMARY
    # ======================================================

    st.subheader(
        "📋 Final Summary"
    )

    summary_df = pd.DataFrame(
        {
            "Parameter": [
                "Skill Match",
                "Experience Match",
                "Education Match",
                "Project Match",
                "Final Suitability",
                "Category"
            ],

            "Result": [
                f"{skill_score:.2f}%",
                f"{experience_score:.2f}%",
                f"{education_score:.2f}%",
                f"{project_score:.2f}%",
                f"{final_score:.2f}/100",
                category
            ]
        }
    )

    st.table(
        summary_df
    )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "AI-Based Resume Analyzer | "
    "LangChain + Gemini + Fuzzy Logic + Streamlit"
)