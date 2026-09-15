# fuzzy_logic.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def create_fuzzy_system():

    # ==========================================
    # 1. INPUT VARIABLES
    # ==========================================

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

    # ==========================================
    # 2. OUTPUT VARIABLE
    # ==========================================

    suitability = ctrl.Consequent(
        np.arange(0, 101, 1),
        "suitability"
    )

    # ==========================================
    # 3. MEMBERSHIP FUNCTIONS
    # ==========================================

    # ---------- Skill Match ----------

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

    # ---------- Experience Match ----------

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

    # ---------- Education Match ----------

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

    # ---------- Project Match ----------

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

    # ==========================================
    # 4. OUTPUT MEMBERSHIP FUNCTIONS
    # ==========================================

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

    # ==========================================
    # 5. FUZZY RULES
    # ==========================================

    # Rule 1
    rule1 = ctrl.Rule(
        skill_match["high"]
        & experience_match["high"]
        & education_match["high"]
        & project_match["high"],
        suitability["excellent"]
    )

    # Rule 2
    rule2 = ctrl.Rule(
        skill_match["high"]
        & experience_match["medium"]
        & project_match["high"],
        suitability["good"]
    )

    # Rule 3
    rule3 = ctrl.Rule(
        skill_match["high"]
        & education_match["high"]
        & project_match["medium"],
        suitability["good"]
    )

    # Rule 4
    rule4 = ctrl.Rule(
        skill_match["medium"]
        & experience_match["medium"]
        & education_match["high"],
        suitability["moderate"]
    )

    # Rule 5
    rule5 = ctrl.Rule(
        skill_match["medium"]
        & project_match["medium"],
        suitability["moderate"]
    )

    # Rule 6
    rule6 = ctrl.Rule(
        skill_match["low"]
        & experience_match["low"],
        suitability["poor"]
    )

    # Rule 7
    rule7 = ctrl.Rule(
        skill_match["low"]
        & project_match["low"],
        suitability["weak"]
    )

    # Rule 8
    rule8 = ctrl.Rule(
        skill_match["high"]
        & experience_match["low"]
        & project_match["high"],
        suitability["good"]
    )

    # Rule 9
    rule9 = ctrl.Rule(
        education_match["high"]
        & skill_match["medium"]
        & project_match["high"],
        suitability["good"]
    )

    # Rule 10
    rule10 = ctrl.Rule(
        skill_match["medium"]
        & education_match["medium"]
        & project_match["low"],
        suitability["weak"]
    )

    # ==========================================
    # 6. CREATE CONTROL SYSTEM
    # ==========================================

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
        rule10
    ])

    return system


# ==========================================
# 7. FUZZY INFERENCE + DEFUZZIFICATION
# ==========================================

def calculate_suitability(
    skill_score,
    experience_score,
    education_score,
    project_score
):

    system = create_fuzzy_system()

    simulation = ctrl.ControlSystemSimulation(system)

    # Crisp inputs
    simulation.input["skill_match"] = skill_score
    simulation.input["experience_match"] = experience_score
    simulation.input["education_match"] = education_score
    simulation.input["project_match"] = project_score

    # Perform fuzzy inference
    simulation.compute()

    # Defuzzified output
    final_score = simulation.output["suitability"]

    return round(final_score, 2)


# ==========================================
# 8. RESULT CATEGORY
# ==========================================

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