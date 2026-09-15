# llm_chain.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from prompts import (
    RESUME_ANALYSIS_PROMPT,
    JOB_ANALYSIS_PROMPT,
    EXPLANATION_PROMPT
)


def get_llm(api_key):
    """
    Create and return the Gemini LLM.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

    return llm


def analyze_resume(resume_text, api_key):
    """
    Analyze resume using LangChain + Gemini.
    """

    llm = get_llm(api_key)

    prompt = ChatPromptTemplate.from_template(
        RESUME_ANALYSIS_PROMPT
    )

    chain = prompt | llm

    response = chain.invoke({
        "resume_text": resume_text
    })

    return response.content


def analyze_job_description(job_description, api_key):
    """
    Analyze job description using LangChain + Gemini.
    """

    llm = get_llm(api_key)

    prompt = ChatPromptTemplate.from_template(
        JOB_ANALYSIS_PROMPT
    )

    chain = prompt | llm

    response = chain.invoke({
        "job_description": job_description
    })

    return response.content


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
    """
    Generate a conversational explanation
    using LangChain + Gemini.
    """

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

    return response.content