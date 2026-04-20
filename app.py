from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import random
from datetime import datetime

app = Flask(__name__)

# ========================================
# ADVANCED CAREER PREDICTION ENGINE
# ========================================

# Comprehensive skill database
SKILL_DATABASE = {
    "programming_languages": ["python", "java", "javascript", "c++", "c#", "go", "rust", "ruby", "php", "swift", "kotlin", "typescript"],
    "frontend": ["html", "css", "react", "angular", "vue", "nextjs", "tailwind", "bootstrap", "sass", "jquery"],
    "backend": ["django", "flask", "spring", "node.js", "express", "fastapi", "laravel", "asp.net", "rails"],
    "databases": ["sql", "mysql", "postgresql", "mongodb", "redis", "oracle", "firebase", "dynamodb"],
    "cloud_devops": ["aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "linux", "git", "ci/cd"],
    "data_science": ["python", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "matplotlib", "seaborn", "r"],
    "data_analytics": ["sql", "excel", "tableau", "power bi", "python", "statistics", "data visualization", "looker"],
    "ai_ml": ["machine learning", "deep learning", "nlp", "computer vision", "llm", "langchain", "openai", "huggingface"],
    "cybersecurity": ["security", "penetration testing", "ethical hacking", "cryptography", "network security", "siem"],
    "mobile": ["android", "ios", "flutter", "react native", "swift", "kotlin", "xamarin"],
    "soft_skills": ["communication", "leadership", "problem solving", "teamwork", "agile", "project management"]
}

# Career domains with complete information

CAREER_DOMAINS = {
    "Data Analyst": {
        "keywords": ["sql", "excel", "tableau", "power bi", "python", "statistics", "data visualization", "looker", "data cleaning", "pandas"],
        "required_skills": ["sql", "excel", "statistics", "data visualization"],
        "preferred_skills": ["python", "tableau", "power bi", "r", "pandas"],
        "salary_range": {"entry": "65k-85k", "mid": "85k-115k", "senior": "115k-150k"},
        "growth_rate": "+35%",
        "job_demand": "Very High",
        "learning_path": [
            "SQL Mastery",
            "Excel Advanced Features",
            "Data Visualization Tools",
            "Statistics Fundamentals",
            "Python for Data Analysis"
        ],
        "certifications": ["Google Data Analytics", "Microsoft Power BI", "Tableau Desktop Specialist"]
    },
    "Data Analytics": {
        "keywords": ["sql", "excel", "tableau", "power bi", "python", "statistics", "data visualization", "business intelligence", "etl"],
        "required_skills": ["sql", "excel", "data visualization", "statistics"],
        "preferred_skills": ["python", "tableau", "power bi", "etl", "data warehousing"],
        "salary_range": {"entry": "70k-90k", "mid": "90k-120k", "senior": "120k-160k"},
        "growth_rate": "+38%",
        "job_demand": "Very High",
        "learning_path": [
            "SQL for Analytics",
            "Business Intelligence Tools",
            "Data Storytelling",
            "Statistical Analysis",
            "Dashboard Creation"
        ],
        "certifications": ["Microsoft Data Analyst", "Google Business Intelligence", "Tableau Desktop"]
    },
    # ... rest of your domains

    "Python Backend Engineer": {
        "keywords": ["python", "django", "flask", "fastapi", "sql", "postgresql", "api", "rest", "graphql", "git"],
        "required_skills": ["python", "sql", "git", "api development"],
        "preferred_skills": ["django", "flask", "docker", "aws", "mongodb"],
        "salary_range": {"entry": "70k-90k", "mid": "90k-130k", "senior": "130k-180k"},
        "growth_rate": "+32%",
        "job_demand": "Very High",
        "learning_path": [
            "Python Basics & Advanced Concepts",
            "Web Frameworks (Django/Flask)",
            "Database Management",
            "API Development",
            "Docker & Containerization"
        ],
        "certifications": ["Python Institute PCEP", "Meta Backend Certificate", "AWS Certified Developer"]
    },
    "Java Backend Engineer": {
        "keywords": ["java", "spring", "spring boot", "hibernate", "maven", "gradle", "sql", "microservices", "kafka"],
        "required_skills": ["java", "spring", "sql", "git", "maven/gradle"],
        "preferred_skills": ["microservices", "docker", "kubernetes", "aws", "kafka"],
        "salary_range": {"entry": "75k-95k", "mid": "95k-140k", "senior": "140k-190k"},
        "growth_rate": "+28%",
        "job_demand": "Very High",
        "learning_path": [
            "Core Java & OOP Concepts",
            "Spring Framework",
            "Database & Hibernate",
            "Microservices Architecture",
            "Cloud Deployment"
        ],
        "certifications": ["Oracle Java Certification", "Spring Professional", "AWS Certified"]
    },
    "Full Stack Developer": {
        "keywords": ["javascript", "react", "node", "python", "html", "css", "mongodb", "express", "typescript", "next.js"],
        "required_skills": ["javascript", "react", "node.js", "html", "css", "git", "mongodb/sql"],
        "preferred_skills": ["typescript", "next.js", "docker", "aws", "graphql"],
        "salary_range": {"entry": "65k-85k", "mid": "85k-125k", "senior": "125k-170k"},
        "growth_rate": "+35%",
        "job_demand": "Very High",
        "learning_path": [
            "JavaScript/TypeScript Mastery",
            "React & Modern Frontend",
            "Node.js Backend",
            "Database Design",
            "Full Stack Deployment"
        ],
        "certifications": ["Meta Full Stack Certificate", "freeCodeCamp", "AWS Developer"]
    },
    "Frontend Developer": {
        "keywords": ["html", "css", "javascript", "react", "vue", "angular", "typescript", "tailwind", "responsive"],
        "required_skills": ["html", "css", "javascript", "react/vue/angular", "git", "responsive design"],
        "preferred_skills": ["typescript", "next.js", "tailwind", "figma", "jest"],
        "salary_range": {"entry": "60k-80k", "mid": "80k-115k", "senior": "115k-155k"},
        "growth_rate": "+30%",
        "job_demand": "High",
        "learning_path": [
            "HTML5 & CSS3 Mastery",
            "JavaScript ES6+",
            "React Framework",
            "State Management",
            "Performance Optimization"
        ],
        "certifications": ["Meta Frontend Certificate", "Frontend Masters", "Scrum Master"]
    },
    "Data Scientist": {
        "keywords": ["python", "pandas", "numpy", "scikit-learn", "tensorflow", "statistics", "sql", "machine learning"],
        "required_skills": ["python", "pandas", "numpy", "statistics", "sql", "machine learning basics"],
        "preferred_skills": ["tensorflow", "deep learning", "aws", "big data", "tableau"],
        "salary_range": {"entry": "80k-105k", "mid": "105k-150k", "senior": "150k-210k"},
        "growth_rate": "+45%",
        "job_demand": "Extremely High",
        "learning_path": [
            "Python for Data Science",
            "Statistics & Mathematics",
            "Machine Learning Algorithms",
            "Deep Learning",
            "MLOps & Deployment"
        ],
        "certifications": ["IBM Data Science", "Google Professional ML", "AWS ML Specialty"]
    },
    "DevOps Engineer": {
        "keywords": ["docker", "kubernetes", "aws", "azure", "jenkins", "terraform", "linux", "git", "ci/cd", "ansible"],
        "required_skills": ["linux", "docker", "git", "ci/cd basics", "aws/azure basics"],
        "preferred_skills": ["kubernetes", "terraform", "jenkins", "prometheus", "ansible"],
        "salary_range": {"entry": "85k-110k", "mid": "110k-155k", "senior": "155k-200k"},
        "growth_rate": "+40%",
        "job_demand": "Extremely High",
        "learning_path": [
            "Linux Administration",
            "Docker & Containerization",
            "Kubernetes Orchestration",
            "CI/CD Pipelines",
            "Infrastructure as Code"
        ],
        "certifications": ["AWS DevOps Engineer", "CKA", "Terraform Associate"]
    },
    "AI/ML Engineer": {
        "keywords": ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "nlp", "computer vision", "llm"],
        "required_skills": ["python", "machine learning", "deep learning basics", "statistics", "tensorflow/pytorch"],
        "preferred_skills": ["nlp", "computer vision", "langchain", "aws", "mlops"],
        "salary_range": {"entry": "90k-120k", "mid": "120k-170k", "senior": "170k-230k"},
        "growth_rate": "+52%",
        "job_demand": "Extremely High",
        "learning_path": [
            "Advanced Python",
            "Machine Learning Theory",
            "Deep Learning Architectures",
            "NLP/Computer Vision",
            "Model Deployment"
        ],
        "certifications": ["TensorFlow Developer", "AWS ML", "Deep Learning Specialization"]
    },
    "Cloud Architect": {
        "keywords": ["aws", "azure", "gcp", "cloud", "terraform", "kubernetes", "docker", "linux", "networking"],
        "required_skills": ["aws/azure/gcp", "cloud concepts", "linux", "networking basics", "security basics"],
        "preferred_skills": ["terraform", "kubernetes", "python", "ci/cd", "database"],
        "salary_range": {"entry": "95k-125k", "mid": "125k-175k", "senior": "175k-240k"},
        "growth_rate": "+38%",
        "job_demand": "Very High",
        "learning_path": [
            "Cloud Fundamentals",
            "AWS/Azure/GCP Deep Dive",
            "Infrastructure as Code",
            "Security & Compliance",
            "Cost Optimization"
        ],
        "certifications": ["AWS Solutions Architect", "Azure Architect", "Google Cloud Architect"]
    },
    "Cybersecurity Specialist": {
        "keywords": ["security", "penetration testing", "ethical hacking", "network security", "cryptography", "siem", "compliance"],
        "required_skills": ["networking", "linux", "security fundamentals", "python basics", "risk assessment"],
        "preferred_skills": ["penetration testing", "cloud security", "siem tools", "compliance"],
        "salary_range": {"entry": "80k-105k", "mid": "105k-150k", "senior": "150k-200k"},
        "growth_rate": "+35%",
        "job_demand": "Very High",
        "learning_path": [
            "Network Security",
            "Ethical Hacking",
            "Security Tools",
            "Compliance & Governance",
            "Incident Response"
        ],
        "certifications": ["CISSP", "CEH", "Security+", "OSCP"]
    }
}

def predict_career(primary_skill, extra_skills, experience, degree, career_gap):
    """Advanced career prediction with scoring"""
    
    primary = primary_skill.lower().strip()
    extra = [s.lower().strip() for s in extra_skills.split(',') if s.strip()] if extra_skills else []
    all_skills = [primary] + extra
    
    # Score each career domain
    scores = {}
    for domain, info in CAREER_DOMAINS.items():
        score = 0
        for skill in all_skills:
            if skill in info["keywords"]:
                score += 2
            for keyword in info["keywords"]:
                if skill in keyword or keyword in skill:
                    score += 1
        
        # Experience multiplier
        if experience <= 2:
            score = score * 0.8
        elif experience <= 5:
            score = score * 1.0
        else:
            score = score * 1.2
        
        scores[domain] = score
    
    # Get best match
    if scores and max(scores.values()) > 0:
        best_domain = max(scores, key=scores.get)
        confidence = min(int((scores[best_domain] / 20) * 100), 95)
    else:
        best_domain = "Full Stack Developer"
        confidence = 65
    
    return best_domain, confidence

def get_level_info(experience, career_gap):
    """Get career level information"""
    if experience <= 2:
        level = "Entry Level"
        level_icon = "🌱"
        color = "beginner"
        responsibilities = [
            "Learn and implement basic features",
            "Write clean, documented code",
            "Fix bugs and perform testing",
            "Collaborate with senior developers"
        ]
    elif experience <= 5:
        level = "Mid Level"
        level_icon = "📈"
        color = "intermediate"
        responsibilities = [
            "Design and implement features independently",
            "Code review and mentor juniors",
            "Lead small projects",
            "Technical decision making"
        ]
    else:
        level = "Senior Level"
        level_icon = "🏆"
        color = "advanced"
        responsibilities = [
            "Architect complex systems",
            "Technical leadership and mentoring",
            "Strategic planning",
            "Cross-team collaboration"
        ]
    
    return level, level_icon, color, responsibilities

# ========================================
# MARKET SKILLS - REAL-TIME DATA
# ========================================

def get_market_insights():
    """Get current market trends"""
    return {
        "trending_skills": [
            {"name": "Artificial Intelligence", "growth": "+156%", "demand": "Critical", "category": "AI/ML"},
            {"name": "Machine Learning", "growth": "+142%", "demand": "Critical", "category": "AI/ML"},
            {"name": "Data Analytics", "growth": "+95%", "demand": "Critical", "category": "Data"},
            {"name": "Cloud Computing (AWS/Azure)", "growth": "+89%", "demand": "Critical", "category": "Cloud"},
            {"name": "Data Science", "growth": "+78%", "demand": "Very High", "category": "Data"},
            {"name": "Cybersecurity", "growth": "+67%", "demand": "Very High", "category": "Security"},
            {"name": "DevOps", "growth": "+65%", "demand": "Very High", "category": "DevOps"},
            {"name": "Kubernetes", "growth": "+58%", "demand": "High", "category": "DevOps"},
            {"name": "React", "growth": "+52%", "demand": "High", "category": "Frontend"},
            {"name": "Python", "growth": "+48%", "demand": "High", "category": "Programming"},
            {"name": "SQL", "growth": "+46%", "demand": "High", "category": "Database"},
            {"name": "Power BI", "growth": "+44%", "demand": "High", "category": "Data"},
            {"name": "Docker", "growth": "+45%", "demand": "High", "category": "DevOps"},
            {"name": "TensorFlow", "growth": "+43%", "demand": "High", "category": "AI/ML"},
            {"name": "Spring Boot", "growth": "+38%", "demand": "High", "category": "Backend"},
            {"name": "Node.js", "growth": "+36%", "demand": "High", "category": "Backend"},
            {"name": "TypeScript", "growth": "+42%", "demand": "High", "category": "Programming"},
            {"name": "Tableau", "growth": "+41%", "demand": "High", "category": "Data"},
            {"name": "GraphQL", "growth": "+41%", "demand": "Medium", "category": "API"}
        ],
        "top_industries": [
            {"name": "Artificial Intelligence", "growth": "+156%", "jobs": "45,000+"},
            {"name": "Data Analytics", "growth": "+112%", "jobs": "68,000+"},
            {"name": "Cloud Computing", "growth": "+89%", "jobs": "120,000+"},
            {"name": "Cybersecurity", "growth": "+67%", "jobs": "35,000+"},
            {"name": "Data Engineering", "growth": "+72%", "jobs": "28,000+"},
            {"name": "DevOps", "growth": "+65%", "jobs": "42,000+"}
        ],
        "salary_trends": {
            "entry": "$65,000 - $85,000",
            "mid": "$95,000 - $130,000",
            "senior": "$140,000 - $200,000"
        }
    }

# ========================================
# FLASK ROUTES
# ========================================

@app.route("/")
def home():
    market_data = get_market_insights()
    return render_template("index.html", market_data=market_data)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    market_data = get_market_insights()
    
    if request.method == "POST":
        primary_skill = request.form.get("primary_skill", "")
        extra_skills = request.form.get("extra_skills", "")
        experience = int(request.form.get("experience", 0))
        degree = request.form.get("degree", "")
        career_gap = int(request.form.get("career_gap", 0))
        
        # Get prediction
        domain, confidence = predict_career(primary_skill, extra_skills, experience, degree, career_gap)
        
        # Get domain details
        domain_info = CAREER_DOMAINS.get(domain, CAREER_DOMAINS["Full Stack Developer"])
        level, level_icon, level_color, responsibilities = get_level_info(experience, career_gap)
        
        return render_template("result.html",
                             domain=domain,
                             confidence=confidence,
                             level=level,
                             level_icon=level_icon,
                             level_color=level_color,
                             domain_info=domain_info,
                             responsibilities=responsibilities,
                             experience=experience,
                             career_gap=career_gap,
                             primary_skill=primary_skill,
                             market_data=market_data)
    
    return render_template("predict.html", market_data=market_data)

@app.route("/readiness", methods=["GET", "POST"])
def readiness():
    market_data = get_market_insights()
    result = None
    
    if request.method == "POST":
        role = request.form.get("role")
        skills_input = request.form.get("skills", "").lower()
        user_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        
        domain_info = CAREER_DOMAINS.get(role, CAREER_DOMAINS["Full Stack Developer"])
        
        # Check required skills
        matched_required = []
        missing_required = []
        
        for req in domain_info["required_skills"]:
            found = False
            for skill in user_skills:
                if req in skill or skill in req:
                    matched_required.append(req)
                    found = True
                    break
            if not found:
                missing_required.append(req)
        
        # Check preferred skills
        matched_preferred = []
        for pref in domain_info["preferred_skills"]:
            for skill in user_skills:
                if pref in skill or skill in pref:
                    matched_preferred.append(pref)
                    break
        
        # Calculate score
        total_required = len(domain_info["required_skills"])
        score = int((len(matched_required) / total_required) * 100) if total_required > 0 else 0
        
        # Determine status
        if score >= 80:
            status = "Ready for Senior Roles"
            status_icon = "🎯"
        elif score >= 60:
            status = "Ready for Mid-Level Roles"
            status_icon = "📈"
        elif score >= 40:
            status = "Needs Preparation"
            status_icon = "📚"
        else:
            status = "Beginner Level"
            status_icon = "🌱"
        
        result = {
            "role": role,
            "score": score,
            "status": status,
            "status_icon": status_icon,
            "matched_required": matched_required,
            "missing_required": missing_required,
            "matched_preferred": matched_preferred,
            "certifications": domain_info["certifications"],
            "learning_path": domain_info["learning_path"],
            "salary_range": domain_info["salary_range"]
        }
    
    return render_template("readiness.html", result=result, market_data=market_data)

@app.route("/market")
def market():
    market_data = get_market_insights()
    return render_template("market.html", market_data=market_data)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 CAREER INTELLIGENCE PLATFORM")
    print("="*60)
    print("📍 http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(debug=True)
    
if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
     port = int(os.environ.get("PORT", 5000))
     app.run(host="0.0.0.0", port=port, debug=False)