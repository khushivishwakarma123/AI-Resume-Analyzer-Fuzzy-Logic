from matcher import calculate_all_scores


candidate_info = """
1. Candidate Name: Khushi Vishwakarma

2. Education: BSc Information Technology

3. Technical Skills: Python, Java, HTML, CSS, JavaScript, MySQL

4. Programming Languages: Python, Java, C, C++

5. Frameworks and Technologies: React, Android Studio

6. Projects: Coding Ninjas Clone using React and Tailwind, Medical Shopping App using Android and Firebase

7. Work Experience: Not Mentioned

8. Internship Experience: 6 months internship in AI Web Development

9. Certifications: Python Certification
"""


job_info = """
1. Job Title: Full Stack Developer

2. Required Technical Skills: Python, JavaScript, React, HTML, CSS, MySQL

3. Preferred Technical Skills: Git, Firebase

4. Required Education: BSc Information Technology

5. Required Experience: 1 year

6. Important Job Responsibilities: Develop web applications using React and Python, work with databases, create responsive user interfaces and maintain applications.
"""


result = calculate_all_scores(
    candidate_info,
    job_info
)


print("MATCHING RESULTS")
print("---------------------------")

print("Skill Match:", result["skill_match"])
print("Experience Match:", result["experience_match"])
print("Education Match:", result["education_match"])
print("Project Match:", result["project_match"])

print("---------------------------")

print("Final Suitability Score:",
      result["final_score"])