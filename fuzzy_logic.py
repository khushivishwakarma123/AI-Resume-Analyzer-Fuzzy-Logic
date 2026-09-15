# fuzzy_logic.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ============================================================
# 1. CREATE FUZZY SYSTEM
# ============================================================

def create_fuzzy_system():

    # ========================================================
    # INPUT VARIABLES
    # ========================================================

    skill_match = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "skill_match"
    )

    experience_match = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "experience_match"
    )

    education_match = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "education_match"
    )

    project_match = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "project_match"
    )

    # ========================================================
    # OUTPUT VARIABLE
    # ========================================================

    suitability = ctrl.Consequent(
        np.arange(0, 101, 1),
        "suitability"
    )

    # ========================================================
    # 2. INPUT MEMBERSHIP FUNCTIONS
    # ========================================================

    # --------------------------------------------------------
    # Skill Match
    # --------------------------------------------------------

    skill_match["low"] = fuzz.trimf(
        skill_match.universe,
        [0, 0, 40]
    )

    skill_match["medium"] = fuzz.trimf(
        skill_match.universe,
        [20, 50, 80]
    )

    skill_match["high"] = fuzz.trimf(
        skill_match.universe,
        [60, 100, 100]
    )

    # --------------------------------------------------------
    # Experience Match
    # --------------------------------------------------------

    experience_match["low"] = fuzz.trimf(
        experience_match.universe,
        [0, 0, 40]
    )

    experience_match["medium"] = fuzz.trimf(
        experience_match.universe,
        [20, 50, 80]
    )

    experience_match["high"] = fuzz.trimf(
        experience_match.universe,
        [60, 100, 100]
    )

    # --------------------------------------------------------
    # Education Match
    # --------------------------------------------------------

    education_match["low"] = fuzz.trimf(
        education_match.universe,
        [0, 0, 40]
    )

    education_match["medium"] = fuzz.trimf(
        education_match.universe,
        [20, 50, 80]
    )

    education_match["high"] = fuzz.trimf(
        education_match.universe,
        [60, 100, 100]
    )

    # --------------------------------------------------------
    # Project Match
    # --------------------------------------------------------

    project_match["low"] = fuzz.trimf(
        project_match.universe,
        [0, 0, 40]
    )

    project_match["medium"] = fuzz.trimf(
        project_match.universe,
        [20, 50, 80]
    )

    project_match["high"] = fuzz.trimf(
        project_match.universe,
        [60, 100, 100]
    )

    # ========================================================
    # 3. OUTPUT MEMBERSHIP FUNCTIONS
    # ========================================================

    suitability["poor"] = fuzz.trimf(
        suitability.universe,
        [0, 0, 30]
    )

    suitability["weak"] = fuzz.trimf(
        suitability.universe,
        [20, 40, 60]
    )

    suitability["moderate"] = fuzz.trimf(
        suitability.universe,
        [40, 60, 80]
    )

    suitability["good"] = fuzz.trimf(
        suitability.universe,
        [60, 75, 90]
    )

    suitability["excellent"] = fuzz.trimf(
        suitability.universe,
        [80, 100, 100]
    )

    # ========================================================
    # 4. FUZZY RULES
    # ========================================================

    # ========================================================
    # EXCELLENT RULES
    # ========================================================

    rule1 = ctrl.Rule(
        skill_match["high"]
        & experience_match["high"]
        & education_match["high"]
        & project_match["high"],
        suitability["excellent"]
    )

    rule2 = ctrl.Rule(
        skill_match["high"]
        & experience_match["high"]
        & project_match["high"],
        suitability["excellent"]
    )

    rule3 = ctrl.Rule(
        skill_match["high"]
        & education_match["high"]
        & project_match["high"],
        suitability["excellent"]
    )

    # ========================================================
    # GOOD RULES
    # ========================================================

    rule4 = ctrl.Rule(
        skill_match["high"]
        & experience_match["medium"]
        & project_match["high"],
        suitability["good"]
    )

    rule5 = ctrl.Rule(
        skill_match["high"]
        & education_match["high"]
        & project_match["medium"],
        suitability["good"]
    )

    rule6 = ctrl.Rule(
        skill_match["high"]
        & experience_match["low"]
        & project_match["high"],
        suitability["good"]
    )

    rule7 = ctrl.Rule(
        skill_match["medium"]
        & education_match["high"]
        & project_match["high"],
        suitability["good"]
    )

    rule8 = ctrl.Rule(
        skill_match["high"]
        & education_match["medium"]
        & project_match["high"],
        suitability["good"]
    )

    # ========================================================
    # MODERATE RULES
    # ========================================================

    rule9 = ctrl.Rule(
        skill_match["medium"]
        & experience_match["medium"]
        & education_match["high"],
        suitability["moderate"]
    )

    rule10 = ctrl.Rule(
        skill_match["medium"]
        & project_match["medium"],
        suitability["moderate"]
    )

    rule11 = ctrl.Rule(
        skill_match["medium"]
        & education_match["medium"]
        & project_match["medium"],
        suitability["moderate"]
    )

    rule12 = ctrl.Rule(
        skill_match["high"]
        & experience_match["medium"]
        & project_match["medium"],
        suitability["moderate"]
    )

    rule13 = ctrl.Rule(
        skill_match["medium"]
        & experience_match["high"]
        & project_match["medium"],
        suitability["moderate"]
    )

    # ========================================================
    # WEAK RULES
    # ========================================================

    rule14 = ctrl.Rule(
        skill_match["medium"]
        & education_match["medium"]
        & project_match["low"],
        suitability["weak"]
    )

    rule15 = ctrl.Rule(
        skill_match["low"]
        & project_match["medium"],
        suitability["weak"]
    )

    rule16 = ctrl.Rule(
        skill_match["medium"]
        & experience_match["low"]
        & education_match["low"],
        suitability["weak"]
    )

    rule17 = ctrl.Rule(
        skill_match["low"]
        & education_match["medium"]
        & project_match["low"],
        suitability["weak"]
    )

    # ========================================================
    # POOR RULES
    # ========================================================

    rule18 = ctrl.Rule(
        skill_match["low"]
        & experience_match["low"],
        suitability["poor"]
    )

    rule19 = ctrl.Rule(
        skill_match["low"]
        & project_match["low"],
        suitability["poor"]
    )

    rule20 = ctrl.Rule(
        skill_match["low"]
        & education_match["low"]
        & project_match["low"],
        suitability["poor"]
    )

    # ========================================================
    # GENERAL COVERAGE RULES
    # ========================================================

    rule21 = ctrl.Rule(
        skill_match["high"] | experience_match["high"],
        suitability["good"]
    )

    rule22 = ctrl.Rule(
        skill_match["medium"] | project_match["medium"],
        suitability["moderate"]
    )

    rule23 = ctrl.Rule(
        skill_match["low"] | experience_match["low"],
        suitability["poor"]
    )

    # ========================================================
    # 5. CREATE CONTROL SYSTEM
    # ========================================================

    system = ctrl.ControlSystem([
        rule1,
        rule2,
        rule3,
        rule4,
        rule5,
        rule6,
        rule7,
        rule8,
        rule9,
        rule10,
        rule11,
        rule12,
        rule13,
        rule14,
        rule15,
        rule16,
        rule17,
        rule18,
        rule19,
        rule20,
        rule21,
        rule22,
        rule23
    ])

    return system


# ============================================================
# 6. FUZZY INFERENCE + DEFUZZIFICATION
# ============================================================

def calculate_suitability(
    skill_score,
    experience_score,
    education_score,
    project_score
):

    # --------------------------------------------------------
    # Create fuzzy control system
    # --------------------------------------------------------

    system = create_fuzzy_system()

    simulation = ctrl.ControlSystemSimulation(system)

    # --------------------------------------------------------
    # Provide crisp inputs
    # --------------------------------------------------------

    simulation.input["skill_match"] = skill_score

    simulation.input["experience_match"] = experience_score

    simulation.input["education_match"] = education_score

    simulation.input["project_match"] = project_score

    # --------------------------------------------------------
    # Perform fuzzy inference
    # --------------------------------------------------------

    simulation.compute()

    # --------------------------------------------------------
    # Defuzzification
    # --------------------------------------------------------

    if "suitability" not in simulation.output:

        raise ValueError(
            "Fuzzy inference could not produce a suitability score. "
            "Please check the input scores and fuzzy rules."
        )

    final_score = simulation.output["suitability"]

    return round(final_score, 2)


# ============================================================
# 7. RESULT CATEGORY
# ============================================================

def get_category(score):

    if score < 30:

        return "Poor Match"

    elif score < 50:

        return "Weak Match"

    elif score < 70:

        return "Moderate Match"

    elif score < 85:

        return "Good Match"

    else:

        return "Excellent Match"
    # ==========================================================
# FUZZY MEMBERSHIP VALUES
# ==========================================================

def get_membership_values(value):
    """
    Calculate the membership degree of a score
    for Low, Medium and High fuzzy sets.
    """

    value = float(value)

    # LOW
    if value <= 0:
        low = 1.0
    elif value >= 40:
        low = 0.0
    else:
        low = (40 - value) / 40

    # MEDIUM
    if value <= 20 or value >= 80:
        medium = 0.0
    elif value == 50:
        medium = 1.0
    elif value < 50:
        medium = (value - 20) / 30
    else:
        medium = (80 - value) / 30

    # HIGH
    if value <= 60:
        high = 0.0
    elif value >= 100:
        high = 1.0
    else:
        high = (value - 60) / 40

    return {
        "Low": round(low, 3),
        "Medium": round(medium, 3),
        "High": round(high, 3)
    }


# ==========================================================
# GET FUZZY ANALYSIS
# ==========================================================

def get_fuzzy_analysis(
    skill_match,
    experience_match,
    education_match,
    project_match,
    final_score
):
    """
    Return membership values for all fuzzy inputs
    and the final suitability category.
    """

    return {
        "Skill Match": get_membership_values(skill_match),

        "Experience Match": get_membership_values(
            experience_match
        ),

        "Education Match": get_membership_values(
            education_match
        ),

        "Project Match": get_membership_values(
            project_match
        ),

        "Final Score": final_score,

        "Category": get_category(final_score)
    }