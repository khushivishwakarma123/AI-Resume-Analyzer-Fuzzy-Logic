# matcher.py

import re
from fuzzy_logic import calculate_suitability


def normalize_text(text):
    """
    Convert text into lowercase and remove unnecessary symbols.
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_list_items(text, section_name):
    """
    Extract comma-separated or line-separated items
    from an LLM-generated analysis.
    """

    if not text:
        return []

    lines = text.splitlines()
    items = []

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        if section_name.lower() in clean_line.lower():

            if ":" in clean_line:
                content = clean_line.split(":", 1)[1].strip()

                parts = re.split(r",|;|\||•", content)

                for part in parts:
                    part = part.strip()

                    if part and part.lower() not in [
                        "not mentioned",
                        "none"
                    ]:
                        items.append(part)

    return items


def extract_section(text, section_name):
    """
    Extract the text belonging to a particular section.
    """

    if not text:
        return ""

    lines = text.splitlines()
    collecting = False
    section_text = []

    for line in lines:

        clean_line = line.strip()

        if section_name.lower() in clean_line.lower():

            collecting = True

            if ":" in clean_line:
                content = clean_line.split(":", 1)[1].strip()

                if content:
                    section_text.append(content)

            continue

        if collecting:

            if re.match(r"^\d+[\.\)]", clean_line):
                break

            if clean_line:
                section_text.append(clean_line)

    return " ".join(section_text)


def calculate_skill_match(candidate_info, job_info):
    """
    Calculate skill match percentage.

    Required skills receive higher importance than
    preferred skills.
    """

    candidate_text = normalize_text(
        extract_section(candidate_info, "Technical Skills")
        + " "
        + extract_section(candidate_info, "Programming Languages")
        + " "
        + extract_section(candidate_info, "Frameworks and Technologies")
    )

    required_skills = extract_list_items(
        job_info,
        "Required Technical Skills"
    )

    preferred_skills = extract_list_items(
        job_info,
        "Preferred Technical Skills"
    )

    if not required_skills and not preferred_skills:
        return 50.0

    required_score = 0

    if required_skills:

        matched_required = 0

        for skill in required_skills:

            skill_normalized = normalize_text(skill)

            if skill_normalized and skill_normalized in candidate_text:
                matched_required += 1

        required_score = (
            matched_required / len(required_skills)
        ) * 100

    preferred_score = 0

    if preferred_skills:

        matched_preferred = 0

        for skill in preferred_skills:

            skill_normalized = normalize_text(skill)

            if skill_normalized and skill_normalized in candidate_text:
                matched_preferred += 1

        preferred_score = (
            matched_preferred / len(preferred_skills)
        ) * 100

    if required_skills and preferred_skills:

        final_score = (
            required_score * 0.75
            + preferred_score * 0.25
        )

    elif required_skills:

        final_score = required_score

    else:

        final_score = preferred_score

    return round(min(final_score, 100), 2)


def extract_years(text):
    """
    Extract years of experience from text.
    """

    if not text:
        return 0.0

    text = normalize_text(text)

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?",
        r"(\d+(?:\.\d+)?)\s*yrs?"
    ]

    values = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for match in matches:

            try:
                values.append(float(match))
            except ValueError:
                pass

    if values:
        return max(values)

    return 0.0


def calculate_experience_match(candidate_info, job_info):
    """
    Calculate experience match percentage.
    """

    candidate_experience = extract_section(
        candidate_info,
        "Work Experience"
    )

    internship_experience = extract_section(
        candidate_info,
        "Internship Experience"
    )

    job_experience = extract_section(
        job_info,
        "Required Experience"
    )

    candidate_years = extract_years(
        candidate_experience + " " + internship_experience
    )

    required_years = extract_years(job_experience)

    # If the job does not specify experience,
    # give a neutral score.
    if required_years == 0:
        return 70.0

    # If candidate has no experience.
    if candidate_years == 0:
        return 20.0

    score = (candidate_years / required_years) * 100

    return round(min(score, 100), 2)


def calculate_education_match(candidate_info, job_info):
    """
    Calculate education match percentage.
    """

    candidate_education = normalize_text(
        extract_section(candidate_info, "Education")
    )

    required_education = normalize_text(
        extract_section(job_info, "Required Education")
    )

    if not required_education:
        return 70.0

    if not candidate_education:
        return 20.0

    candidate_words = set(candidate_education.split())
    required_words = set(required_education.split())

    if not required_words:
        return 70.0

    matched_words = candidate_words.intersection(
        required_words
    )

    score = (
        len(matched_words) / len(required_words)
    ) * 100

    return round(min(score, 100), 2)


def calculate_project_match(candidate_info, job_info):
    """
    Calculate project relevance based on overlap between
    candidate projects and job responsibilities/skills.
    """

    project_text = normalize_text(
        extract_section(candidate_info, "Projects")
    )

    job_text = normalize_text(
        extract_section(job_info, "Important Job Responsibilities")
        + " "
        + extract_section(job_info, "Required Technical Skills")
        + " "
        + extract_section(job_info, "Preferred Technical Skills")
    )

    if not project_text or not job_text:
        return 50.0

    project_words = set(project_text.split())
    job_words = set(job_text.split())

    # Remove very common words.
    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "using",
        "from",
        "that",
        "this",
        "into",
        "will",
        "have",
        "has",
        "are",
        "was",
        "were",
        "candidate",
        "job"
    }

    project_words -= stop_words
    job_words -= stop_words

    if not job_words:
        return 50.0

    matched_words = project_words.intersection(job_words)

    score = (
        len(matched_words) / len(job_words)
    ) * 100

    return round(min(score, 100), 2)


def calculate_all_scores(candidate_info, job_info):
    """
    Calculate all four matching scores and
    pass them to the fuzzy inference system.
    """

    skill_match = calculate_skill_match(
        candidate_info,
        job_info
    )

    experience_match = calculate_experience_match(
        candidate_info,
        job_info
    )

    education_match = calculate_education_match(
        candidate_info,
        job_info
    )

    project_match = calculate_project_match(
        candidate_info,
        job_info
    )

    final_score = calculate_suitability(
        skill_match,
        experience_match,
        education_match,
        project_match
    )

    return {
        "skill_match": skill_match,
        "experience_match": experience_match,
        "education_match": education_match,
        "project_match": project_match,
        "final_score": final_score
    }