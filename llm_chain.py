from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from prompts import (
    RESUME_ANALYSIS_PROMPT,
    JOB_ANALYSIS_PROMPT,
    EXPLANATION_PROMPT
)


# --------------------------------------------------
# CONVERT GEMINI RESPONSE TO TEXT
# --------------------------------------------------

def response_to_text(response):
    """
    Converts Gemini/LangChain response content into
    a normal string.

    Newer Gemini responses may sometimes return
    content as a list instead of a string.
    """

    content = response.content

    # Normal string response
    if isinstance(content, str):
        return content

    # List response
    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict):

                if "text" in item:
                    text_parts.append(str(item["text"]))

            else:
                text_parts.append(str(item))

        return "\n".join(text_parts)

    # Any other format
    return str(content)


# --------------------------------------------------
# CREATE GEMINI LLM
# --------------------------------------------------

def get_llm(api_key):

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key
    )

    return llm


# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------

def analyze_resume(resume_text, api_key):

    llm = get_llm(api_key)

    prompt = ChatPromptTemplate.from_template(
        RESUME_ANALYSIS_PROMPT
    )

    chain = prompt | llm

    response = chain.invoke({
        "resume_text": resume_text
    })

    return response_to_text(response)


# --------------------------------------------------
# ANALYZE JOB DESCRIPTION
# --------------------------------------------------

def analyze_job_description(job_description, api_key):

    llm = get_llm(api_key)

    prompt = ChatPromptTemplate.from_template(
        JOB_ANALYSIS_PROMPT
    )

    chain = prompt | llm

    response = chain.invoke({
        "job_description": job_description
    })

    return response_to_text(response)


# --------------------------------------------------
# GENERATE AI EXPLANATION
# --------------------------------------------------

def generate_explanation(
    skill_match,
    experience_match,
    education_match,
    project_match,
    final_score,
    category,
    candidate_info,
    job_info,
    api_key
):

    llm = get_llm(api_key)

    prompt = ChatPromptTemplate.from_template(
        EXPLANATION_PROMPT
    )

    chain = prompt | llm

    response = chain.invoke({

        "skill_match": skill_match,

        "experience_match": experience_match,

        "education_match": education_match,

        "project_match": project_match,

        "final_score": final_score,

        "category": category,

        "candidate_info": candidate_info,

        "job_info": job_info
    })

    return response_to_text(response)