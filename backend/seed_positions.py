from app.database import SessionLocal
from app.models import JobPosition


POSITIONS = [
    {
        "title": "Senior AI/ML Engineer",
        "description": "Lead end-to-end ML lifecycle, deploy deep learning systems, optimize model performance, mentor engineers.",
        "required_skills": {"keywords": ["python", "pytorch", "mlops", "docker", "aws", "nlp"]},
        "experience_years": 5,
        "education": "BS/MS in CS, AI, or related field",
    },
    {
        "title": "Junior Python Developer",
        "description": "Build Python backend services, write APIs, tests, and collaborate with data teams.",
        "required_skills": {"keywords": ["python", "fastapi", "sqlalchemy", "pytest", "git"]},
        "experience_years": 1,
        "education": "BS in CS or equivalent",
    },
    {
        "title": "ML Ops Engineer",
        "description": "Manage CI/CD for ML, containerize workloads, monitor model drift, automate training pipelines.",
        "required_skills": {"keywords": ["mlflow", "docker", "kubernetes", "python", "redis", "celery"]},
        "experience_years": 3,
        "education": "BS in CS/Data Engineering",
    },
    {
        "title": "Backend Engineer (Python)",
        "description": "Design high-performance backend APIs, optimize database queries, ensure reliability and observability.",
        "required_skills": {"keywords": ["python", "postgresql", "fastapi", "redis", "microservices"]},
        "experience_years": 3,
        "education": "BS in Software Engineering",
    },
    {
        "title": "Data Scientist",
        "description": "Build predictive models, perform feature engineering, and communicate insights to stakeholders.",
        "required_skills": {"keywords": ["python", "pandas", "scikit-learn", "statistics", "visualization"]},
        "experience_years": 2,
        "education": "BS/MS in Data Science, Statistics, or related",
    },
]


if __name__ == "__main__":
    db = SessionLocal()
    try:
        for p in POSITIONS:
            exists = db.query(JobPosition).filter(JobPosition.title == p["title"]).first()
            if not exists:
                db.add(JobPosition(**p))
        db.commit()
        print("Seed complete")
    finally:
        db.close()
