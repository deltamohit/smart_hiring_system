# auth.py
import streamlit as st
import bcrypt
from database import (
    insert_student, fetch_student,
    insert_placement_officer, fetch_placement_officer
)


def hash_password(password):
    """Hash password using bcrypt for security"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed):
    """Verify password against stored hash"""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False


# ============ STUDENT SIGNUP ============

def student_signup():
    """Student registration form"""
    st.subheader("🎓 Student Registration")
    
    with st.form("student_signup_form", clear_on_submit=True):
        name = st.text_input("Full Name*", placeholder="e.g., Mohit Kumar")
        email = st.text_input("Email*", placeholder="e.g., mohit@sctce.ac.in")
        password = st.text_input("Password*", type="password", placeholder="Min 6 characters")
        confirm_password = st.text_input("Confirm Password*", type="password")
        
        year = st.selectbox("Year of Study*", [
            "Select Year",
            "1st Year", 
            "2nd Year", 
            "3rd Year", 
            "4th Year"
        ])
        
        branch = st.selectbox("Branch*", [
            "Select Branch",
            "Computer Science & Engineering",
            "Electronics & Communication Engineering",
            "Electrical & Electronics Engineering",
            "Mechanical Engineering",
            "Civil Engineering"
        ])
        
        submit = st.form_submit_button("Sign Up as Student", use_container_width=True)
        
        if submit:
            # Validation
            if not name or not email or not password:
                st.error("❌ Please fill all required fields!")
                return
            
            if year == "Select Year" or branch == "Select Branch":
                st.error("❌ Please select your Year and Branch!")
                return
            
            if password != confirm_password:
                st.error("❌ Passwords don't match!")
                return
            
            if len(password) < 6:
                st.error("❌ Password must be at least 6 characters!")
                return
            
            # Check if email already exists
            existing_student = fetch_student(email)
            if existing_student:
                st.error("❌ Email already registered as student!")
                return
            
            # Create new student account
            hashed = hash_password(password)
            result = insert_student(email, name, hashed, year, branch)
            
            if result:
                st.success("✅ Student account created successfully! Please login.")
                st.balloons()
            else:
                st.error("❌ Error creating account. Please try again.")


# ============ PLACEMENT CELL SIGNUP ============

def placement_signup():
    """Placement Cell registration form"""
    st.subheader("🏢 Placement Cell Registration")
    
    with st.form("placement_signup_form", clear_on_submit=True):
        name = st.text_input("Full Name*", placeholder="e.g., Dr. John Doe")
        email = st.text_input("Email*", placeholder="e.g., placement@sctce.ac.in")
        password = st.text_input("Password*", type="password", placeholder="Min 6 characters")
        confirm_password = st.text_input("Confirm Password*", type="password")
        
        submit = st.form_submit_button("Sign Up as Placement Cell", use_container_width=True)
        
        if submit:
            # Validation
            if not name or not email or not password:
                st.error("❌ Please fill all required fields!")
                return
            
            if password != confirm_password:
                st.error("❌ Passwords don't match!")
                return
            
            if len(password) < 6:
                st.error("❌ Password must be at least 6 characters!")
                return
            
            # Check if email already exists
            existing_officer = fetch_placement_officer(email)
            if existing_officer:
                st.error("❌ Email already registered as placement cell!")
                return
            
            # Create new placement officer account
            hashed = hash_password(password)
            result = insert_placement_officer(email, name, hashed)
            
            if result:
                st.success("✅ Placement Cell account created successfully! Please login.")
                st.balloons()
            else:
                st.error("❌ Error creating account. Please try again.")


# ============ STUDENT LOGIN ============

def student_login():
    """Student login form"""
    st.subheader("🎓 Student Login")
    
    with st.form("student_login_form"):
        email = st.text_input("Email", placeholder="e.g., mohit@sctce.ac.in")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login as Student", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("❌ Please enter both email and password!")
                return
            
            # Fetch student data
            student = fetch_student(email)
            
            if student and verify_password(password, student['password']):
                # Login successful
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = 'student'
                st.session_state['user_email'] = email
                st.session_state['user_name'] = student['name']
                st.session_state['year'] = student['year']
                st.session_state['branch'] = student['branch']
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password!")


# ============ PLACEMENT CELL LOGIN ============

def placement_login():
    """Placement Cell login form"""
    st.subheader("🏢 Placement Cell Login")
    
    with st.form("placement_login_form"):
        email = st.text_input("Email", placeholder="e.g., placement@sctce.ac.in")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login as Placement Cell", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("❌ Please enter both email and password!")
                return
            
            # Fetch placement officer data
            officer = fetch_placement_officer(email)
            
            if officer and verify_password(password, officer['password']):
                # Login successful
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = 'placement_cell'
                st.session_state['user_email'] = email
                st.session_state['user_name'] = officer['name']
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password!")


# ============ LOGOUT ============

def logout():
    """Logout user and clear all session data"""
    st.session_state['logged_in'] = False
    st.session_state['user_type'] = None
    st.session_state['user_email'] = None
    st.session_state['user_name'] = None
    
    # Clear student-specific data if exists
    if 'year' in st.session_state:
        del st.session_state['year']
    if 'branch' in st.session_state:
        del st.session_state['branch']
    
    st.rerun()


# ============ AUTHENTICATION CHECK ============

def require_auth():
    """Check if user is logged in"""
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        return False
    return True
