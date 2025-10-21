# matcher.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from company_database import COMPANY_JOB_SKILLS, SKILL_COURSE_MAP

# Load the S-BERT model (this happens once when the module is imported)
print("Loading S-BERT model... (this may take a moment)")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("S-BERT model loaded successfully!")

def match_resume_to_job(processed_resume_text, company_name, job_role):
    """
    Complete matching function using company-specific job role skills.
    
    Args:
        processed_resume_text (str): The preprocessed resume text.
        company_name (str): The company name
        job_role (str): The job role to match against.
    
    Returns:
        dict: Complete matching results with scores and feedback.
    """
    # Get skills for this specific company and job role
    if company_name not in COMPANY_JOB_SKILLS:
        return {'error': f"Company '{company_name}' not found in database."}
    
    if job_role not in COMPANY_JOB_SKILLS[company_name]:
        return {'error': f"Job role '{job_role}' not found for {company_name}."}
    
    required_skills = COMPANY_JOB_SKILLS[company_name][job_role]
    
    # Calculate ATS score (keyword matching)
    matched_skills = []
    missing_skills = []
    
    for skill in required_skills:
        if skill in processed_resume_text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    ats_score = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0
    
    # Calculate semantic similarity
    job_description_text = f"Required skills for {job_role} at {company_name}: {', '.join(required_skills)}."
    resume_embedding = model.encode([processed_resume_text])
    job_embedding = model.encode([job_description_text])
    similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
    semantic_score = similarity * 100
    
    # Get feedback
    feedback = {}
    for skill in missing_skills:
        if skill in SKILL_COURSE_MAP:
            feedback[skill] = SKILL_COURSE_MAP[skill]
        else:
            feedback[skill] = f"Consider learning about '{skill}' through online resources."
    
    # Combined score
    combined_score = (ats_score + semantic_score) / 2
    
    return {
        'company': company_name,
        'job_role': job_role,
        'ats_score': float(round (ats_score, 2)),
        'semantic_score': float(round(semantic_score, 2)),
        'combined_score': float(round(combined_score, 2)),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'total_skills': len(required_skills),
        'feedback': feedback
    }
