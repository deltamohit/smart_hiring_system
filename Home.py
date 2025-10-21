# Home.py
import streamlit as st
from auth import (
    student_signup, placement_signup,
    student_login, placement_login,
    logout
)

# Page configuration
st.set_page_config(
    page_title="CGPU BUDDY- SCT College",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_type'] = None
    st.session_state['user_email'] = None
    st.session_state['user_name'] = None

# ============ MAIN APP LOGIC ============

if not st.session_state['logged_in']:
    # User is NOT logged in - Show Login/Signup page
    
    st.title("🎓CGPU BUDDY")
    st.subheader("SCT College of Engineering - Placement Portal")
    st.write("---")
    
    # Create tabs for Login and Signup
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    # ===== LOGIN TAB =====
    with tab1:
        st.write("### Login to Your Account")
        st.info("📌 Select your account type below:")
        
        # Create two columns for Student and Placement Cell login
        col1, col2 = st.columns(2)
        
        with col1:
            student_login()
        
        with col2:
            placement_login()
    
    # ===== SIGNUP TAB =====
    with tab2:
        st.write("### Create New Account")
        st.info("📌 Register as a Student or Placement Cell Officer:")
        
        # Create two columns for Student and Placement Cell signup
        col1, col2 = st.columns(2)
        
        with col1:
            student_signup()
        
        with col2:
            placement_signup()

else:
    # User IS logged in - Show main application
    
    # Sidebar with user info
    st.sidebar.success(f"✅ Logged in as: **{st.session_state['user_name']}**")
    st.sidebar.info(f"👤 Account Type: **{st.session_state['user_type'].replace('_', ' ').title()}**")
    
    # Show student-specific info
    if st.session_state['user_type'] == 'student':
        st.sidebar.write(f"📚 Year: **{st.session_state['year']}**")
        st.sidebar.write(f"🎓 Branch: **{st.session_state['branch']}**")
    
    st.sidebar.write("---")
    
    # Logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()
    
    # Main content - your original welcome page
    st.markdown('<p style="font-size:50px; font-weight:bold; text-align:center">📄 Smart Hiring System</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:25px; text-align:center">Sree Chitra Thirunal College of Engineering</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # Content based on user type
    if st.session_state['user_type'] == 'student':
        st.markdown("## 🎓 Welcome, Student!")
        
        st.markdown("""
        ### 📋 What You Can Do:
        
        #### 👨‍🎓 For Students
        - **Company-Based Matching**: Select companies that visited last year
        - **AI-Powered Analysis**: Get ATS and Semantic similarity scores
        - **Skill Gap Analysis**: Identify missing skills for your target role
        - **Personalized Recommendations**: Get course suggestions to improve
        
        ### 🚀 How to Get Started:
        1. Navigate to **👨‍🎓 Student Mode** from the sidebar
        2. Select a company that visited last year
        3. Choose the specific job role
        4. Upload your resume (PDF format)
        5. Click **Analyze Resume** to get your match score and recommendations
        """)
        
    elif st.session_state['user_type'] == 'placement_cell':
        st.markdown("## 🏢 Welcome, Placement Cell!")
        
        st.markdown("""
        ### 📋 What You Can Do:
        
        #### 🏢 For Placement Unit
        - **Student Rankings**: Rank all applicants for a specific company
        - **Comparative Analysis**: See how students stack up against each other
        - **Data Export**: Download rankings as CSV for records
        - **Placement Insights**: Based on 2025 batch placement data
        
        ### 🚀 How to Get Started:
        1. Navigate to **🏢 Placement Unit Mode** from the sidebar
        2. Select a company and job role
        3. View real-time rankings of all applicants
        4. Export data for placement records
        """)
    
    st.divider()
    
    # Statistics (visible to all logged-in users)
    st.markdown("## 📊 Placement Statistics (2025 Batch)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Students Placed", value="229")
    
    with col2:
        st.metric(label="Companies Visited", value="40")
    
    with col3:
        st.metric(label="Highest CTC", value="₹34.0 L")
    
    with col4:
        st.metric(label="Average CTC", value="₹4.5 L")
    
    st.divider()
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p>Built with ❤️ using Streamlit, S-BERT, and NLTK</p>
        <p><small>Smart Hiring System v2.0 | Integrated with SCT Placement Data 2025</small></p>
    </div>
    """, unsafe_allow_html=True)
