# matcher.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from data_manager import JOB_SKILL_DATABASE, SKILL_COURSE_MAP

# Load the S-BERT model (this happens once when the module is imported)
print("Loading S-BERT model... (this may take a moment)")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("S-BERT model loaded successfully!")

def calculate_ats_score(processed_resume_text, job_role):
    """
    Calculates an ATS-like keyword match score.
    Counts how many required skills for the job role are present in the resume.
    
    Args:
        processed_resume_text (str): The preprocessed resume text.
        job_role (str): The job role to match against (must be a key in JOB_SKILL_DATABASE).
    
    Returns:
        dict: Contains 'score' (percentage), 'matched_skills', 'missing_skills', and 'total_skills'.
    """
    if job_role not in JOB_SKILL_DATABASE:
        return {
            'score': 0,
            'matched_skills': [],
            'missing_skills': [],
            'total_skills': 0,
            'error': f"Job role '{job_role}' not found in database."
        }
    
    required_skills = JOB_SKILL_DATABASE[job_role]
    total_skills = len(required_skills)
    
    matched_skills = []
    missing_skills = []
    
    for skill in required_skills:
        if skill in processed_resume_text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    score_percentage = (len(matched_skills) / total_skills) * 100 if total_skills > 0 else 0
    
    return {
        'score': round(score_percentage, 2),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'total_skills': total_skills
    }

def calculate_semantic_similarity(processed_resume_text, job_role):
    """
    Calculates semantic similarity between resume and job role using S-BERT embeddings.
    
    Args:
        processed_resume_text (str): The preprocessed resume text.
        job_role (str): The job role to match against.
    
    Returns:
        dict: Contains 'similarity_score' (0-100 scale).
    """
    if job_role not in JOB_SKILL_DATABASE:
        return {
            'similarity_score': 0,
            'error': f"Job role '{job_role}' not found in database."
        }
    
    # Create a descriptive sentence from the job role skills
    required_skills = JOB_SKILL_DATABASE[job_role]
    job_description_text = f"Required skills for a {job_role} include: {', '.join(required_skills)}."
    
    # Generate embeddings
    resume_embedding = model.encode([processed_resume_text])
    job_embedding = model.encode([job_description_text])
    
    # Calculate cosine similarity
    similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
    
    # Convert to percentage (0-100 scale)
    similarity_percentage = similarity * 100
    
    return {
        'similarity_score': round(similarity_percentage, 2)
    }

def get_personalized_feedback(missing_skills):
    """
    Generates personalized course recommendations for missing skills.
    
    Args:
        missing_skills (list): List of skills the resume is missing.
    
    Returns:
        dict: Maps each missing skill to a course recommendation.
    """
    feedback = {}
    for skill in missing_skills:
        if skill in SKILL_COURSE_MAP:
            feedback[skill] = SKILL_COURSE_MAP[skill]
        else:
            feedback[skill] = f"Consider learning about '{skill}' through online resources."
    
    return feedback

def match_resume_to_job(processed_resume_text, job_role):
    """
    Complete matching function that combines ATS score, semantic similarity, and feedback.
    
    Args:
        processed_resume_text (str): The preprocessed resume text.
        job_role (str): The job role to match against.
    
    Returns:
        dict: Complete matching results with scores and feedback.
    """
    # Calculate ATS score
    ats_result = calculate_ats_score(processed_resume_text, job_role)
    
    # Calculate semantic similarity
    semantic_result = calculate_semantic_similarity(processed_resume_text, job_role)
    
    # Get personalized feedback for missing skills
    feedback = get_personalized_feedback(ats_result['missing_skills'])
    
    # Calculate combined score (simple average of ATS and semantic scores)
    combined_score = (ats_result['score'] + semantic_result['similarity_score']) / 2
    
    return {
        'job_role': job_role,
        'ats_score': ats_result['score'],
        'semantic_score': semantic_result['similarity_score'],
        'combined_score': round(combined_score, 2),
        'matched_skills': ats_result['matched_skills'],
        'missing_skills': ats_result['missing_skills'],
        'total_skills': ats_result['total_skills'],
        'feedback': feedback
    }
