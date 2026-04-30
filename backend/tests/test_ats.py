from app.services.ats_scorer import calculate_ats_score


def test_ats_scoring_is_deterministic():
    cv = "Experience 5 years python fastapi mlops. Skills python docker aws. Education BS."
    jd = "Need python fastapi docker aws mlops engineer with 5 years experience."
    s1 = calculate_ats_score(cv, jd, 5)
    s2 = calculate_ats_score(cv, jd, 5)
    assert s1 == s2
