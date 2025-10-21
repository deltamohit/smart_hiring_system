# database.py
import os
from supabase import create_client, Client

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============ STUDENT FUNCTIONS ============

def insert_student(email, name, password_hash, year, branch):
    """Register a new student in the database"""
    try:
        response = supabase.table('students').insert({
            "email": email,
            "name": name,
            "password": password_hash,
            "year": year,
            "branch": branch
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error inserting student: {e}")
        return None


def fetch_student(email):
    """Get student data by email"""
    try:
        response = supabase.table('students').select("*").eq('email', email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching student: {e}")
        return None


def get_all_students():
    """Get all students from database"""
    try:
        response = supabase.table('students').select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching all students: {e}")
        return []


# ============ PLACEMENT CELL FUNCTIONS ============

def insert_placement_officer(email, name, password_hash):
    """Register a new placement cell officer in the database"""
    try:
        response = supabase.table('placement_officers').insert({
            "email": email,
            "name": name,
            "password": password_hash
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error inserting placement officer: {e}")
        return None


def fetch_placement_officer(email):
    """Get placement officer data by email"""
    try:
        response = supabase.table('placement_officers').select("*").eq('email', email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching placement officer: {e}")
        return None
# Add to database.py

# ============ RESUME MANAGEMENT FUNCTIONS ============

def save_student_resume(student_email, resume_text, filename):
    """Save a new resume version for student"""
    try:
        # Get current max version number
        response = supabase.table('student_resumes').select('version_number').eq('student_email', student_email).order('version_number', desc=True).limit(1).execute()
        
        next_version = 1
        if response.data and len(response.data) > 0:
            next_version = response.data[0]['version_number'] + 1
            
            # Mark all previous resumes as not current
            supabase.table('student_resumes').update({'is_current': False}).eq('student_email', student_email).execute()
        
        # Insert new resume
        result = supabase.table('student_resumes').insert({
            'student_email': student_email,
            'resume_text': resume_text,
            'resume_filename': filename,
            'version_number': next_version,
            'is_current': True
        }).execute()
        
        return result.data
    except Exception as e:
        print(f"Error saving resume: {e}")
        return None


def get_current_resume(student_email):
    """Get student's current/latest resume"""
    try:
        response = supabase.table('student_resumes').select('*').eq('student_email', student_email).eq('is_current', True).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching current resume: {e}")
        return None


def get_all_resume_versions(student_email):
    """Get all resume versions for a student"""
    try:
        response = supabase.table('student_resumes').select('*').eq('student_email', student_email).order('version_number', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching resume versions: {e}")
        return []


# ============ ANALYSIS HISTORY FUNCTIONS ============

def save_analysis_result(student_email, company_name, job_role, resume_version, resume_filename, 
                         ats_score, semantic_score, combined_score, matched_skills, missing_skills, feedback):
    """Save analysis result to history"""
    try:
        result = supabase.table('analysis_history').insert({
            'student_email': student_email,
            'company_name': company_name,
            'job_role': job_role,
            'resume_version': resume_version,
            'resume_filename': resume_filename,
            'ats_score': ats_score,
            'semantic_score': semantic_score,
            'combined_score': combined_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'feedback': feedback
        }).execute()
        return result.data
    except Exception as e:
        print(f"Error saving analysis: {e}")
        return None


def get_student_analysis_history(student_email):
    """Get all analysis history for a student, grouped by company"""
    try:
        response = supabase.table('analysis_history').select('*').eq('student_email', student_email).order('analyzed_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching analysis history: {e}")
        return []


def get_company_specific_history(student_email, company_name):
    """Get all analyses for a specific company"""
    try:
        response = supabase.table('analysis_history').select('*').eq('student_email', student_email).eq('company_name', company_name).order('analyzed_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching company history: {e}")
        return []


def get_latest_analysis_for_company(student_email, company_name):
    """Get the most recent analysis for a company"""
    try:
        response = supabase.table('analysis_history').select('*').eq('student_email', student_email).eq('company_name', company_name).order('analyzed_at', desc=True).limit(1).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching latest analysis: {e}")
        return None
# ============ ANNOUNCEMENT FUNCTIONS ============

def create_announcement(title, message, posted_by_email, posted_by_name):
    """Create a new announcement from placement cell"""
    try:
        result = supabase.table('announcements').insert({
            'title': title,
            'message': message,
            'posted_by': posted_by_email,
            'posted_by_name': posted_by_name,
            'is_active': True
        }).execute()
        return result.data
    except Exception as e:
        print(f"Error creating announcement: {e}")
        return None


def get_active_announcements():
    """Get all active announcements (for students to see)"""
    try:
        response = supabase.table('announcements').select('*').eq('is_active', True).order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching announcements: {e}")
        return []


def get_all_announcements():
    """Get all announcements (for placement cell to manage)"""
    try:
        response = supabase.table('announcements').select('*').order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching all announcements: {e}")
        return []


def delete_announcement(announcement_id):
    """Delete an announcement"""
    try:
        result = supabase.table('announcements').delete().eq('id', announcement_id).execute()
        return result.data
    except Exception as e:
        print(f"Error deleting announcement: {e}")
        return None


def toggle_announcement_status(announcement_id, is_active):
    """Activate or deactivate an announcement"""
    try:
        result = supabase.table('announcements').update({'is_active': is_active}).eq('id', announcement_id).execute()
        return result.data
    except Exception as e:
        print(f"Error toggling announcement: {e}")
        return None

# ============ PUBLISHED RANKINGS FUNCTIONS ============

def publish_ranking(title, company_name, job_role, description, rankings, published_by_email, published_by_name):
    """Publish student rankings for a company/role"""
    try:
        result = supabase.table('published_rankings').insert({
            'title': title,
            'company_name': company_name,
            'job_role': job_role,
            'description': description,
            'rankings': rankings,  # JSON format
            'published_by': published_by_email,
            'published_by_name': published_by_name,
            'is_active': True
        }).execute()
        return result.data
    except Exception as e:
        print(f"Error publishing ranking: {e}")
        return None


def get_active_rankings():
    """Get all active published rankings"""
    try:
        response = supabase.table('published_rankings').select('*').eq('is_active', True).order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching rankings: {e}")
        return []


def get_all_rankings():
    """Get all published rankings (for placement cell)"""
    try:
        response = supabase.table('published_rankings').select('*').order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching all rankings: {e}")
        return []


def delete_ranking(ranking_id):
    """Delete a published ranking"""
    try:
        result = supabase.table('published_rankings').delete().eq('id', ranking_id).execute()
        return result.data
    except Exception as e:
        print(f"Error deleting ranking: {e}")
        return None


def get_all_student_analyses(company_name, job_role):
    """Get all student analyses for a specific company and job role"""
    try:
        response = supabase.table('analysis_history').select('*').eq('company_name', company_name).eq('job_role', job_role).order('combined_score', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching student analyses: {e}")
        return []
def get_all_student_analyses(company_name, job_role):
    """Get LATEST analysis per student for a specific company and job role"""
    try:
        # Get all analyses for this company/role
        response = supabase.table('analysis_history').select('*').eq('company_name', company_name).eq('job_role', job_role).order('analyzed_at', desc=True).execute()
        
        if not response.data:
            return []
        
        # Filter to get only the LATEST analysis per student
        seen_students = set()
        latest_analyses = []
        
        for analysis in response.data:
            student_email = analysis['student_email']
            if student_email not in seen_students:
                seen_students.add(student_email)
                latest_analyses.append(analysis)
        
        # Sort by combined score descending
        latest_analyses.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return latest_analyses
    except Exception as e:
        print(f"Error fetching student analyses: {e}")
        return []
def get_student_by_email(email):
    """Get student details by email"""
    try:
        response = supabase.table('students').select('*').eq('email', email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching student: {e}")
        return None

