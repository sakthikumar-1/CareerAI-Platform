def calculate_readiness(predicted_domain, known_skills, role_skill_map):

    required_skills = role_skill_map.get(predicted_domain, [])

    match_count = sum(1 for skill in known_skills if skill in required_skills)

    total_required = len(required_skills)

    probability = (match_count / total_required) * 100

    return round(probability, 2)
