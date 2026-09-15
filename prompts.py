# prompts.py

RESUME_ANALYSIS_PROMPT = """
You are an expert resume analyzer.

Analyze the candidate's resume and extract useful information.

Resume:
{resume_text}

Extract the following information:

1. Candidate Name
2. Education
3. Technical Skills
4. Programming Languages
5. Frameworks and Technologies
6. Projects
7. Work Experience
8. Internship Experience
9. Certifications

Important instructions:
- Only use information present in the resume.
- Do not invent or assume information.
- If something is not available, write "Not Mentioned".
- Keep the answer clear and structured.
"""


JOB_ANALYSIS_PROMPT = """
You are an expert job description analyzer.

Analyze the following job description:

{job_description}

Extract the following information:

1. Job Title
2. Required Technical Skills
3. Preferred Technical Skills
4. Required Education
5. Required Experience
6. Important Job Responsibilities

Important instructions:
- Only use information present in the job description.
- Do not invent requirements.
- If something is not mentioned, write "Not Mentioned".
- Keep the answer clear and structured.
"""


EXPLANATION_PROMPT = """
You are an AI career advisor.

A candidate's resume was compared with a job description.

The fuzzy logic system calculated the following scores:

Skill Match: {skill_match}/100
Experience Match: {experience_match}/100
Education Match: {education_match}/100
Project Match: {project_match}/100

Final Job Suitability Score:
{final_score}/100

Suitability Category:
{category}

Candidate Information:
{candidate_info}

Job Information:
{job_info}

Provide a simple and professional explanation.

Your response must include:

1. Overall Assessment
2. Candidate Strengths
3. Areas for Improvement
4. Practical Recommendations

Do not say that the candidate is guaranteed to get the job.

Explain the result in a way that a student can easily understand.
"""