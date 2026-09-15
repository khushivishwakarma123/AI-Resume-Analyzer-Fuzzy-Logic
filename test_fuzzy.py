from fuzzy_logic import calculate_suitability, get_category


# Test Case 1 - Strong candidate
score1 = calculate_suitability(
    skill_score=90,
    experience_score=85,
    education_score=95,
    project_score=90
)

print("Test Case 1")
print("Suitability Score:", score1)
print("Category:", get_category(score1))
print()


# Test Case 2 - Average candidate
score2 = calculate_suitability(
    skill_score=65,
    experience_score=50,
    education_score=80,
    project_score=60
)

print("Test Case 2")
print("Suitability Score:", score2)
print("Category:", get_category(score2))
print()


# Test Case 3 - Weak candidate
score3 = calculate_suitability(
    skill_score=20,
    experience_score=20,
    education_score=30,
    project_score=15
)

print("Test Case 3")
print("Suitability Score:", score3)
print("Category:", get_category(score3))