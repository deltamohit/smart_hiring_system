# Home.py
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Smart Hiring System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
        text-align: center;
    }
    .medium-font {
        font-size:25px !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.markdown('<p class="big-font">📄 Smart Hiring System</p>', unsafe_allow_html=True)
st.markdown('<p class="medium-font">Sree Chitra Thirunal College of Engineering</p>', unsafe_allow_html=True)

st.divider()

# Introduction
st.markdown("""
## 🎯 Welcome to the Smart Hiring System!

This intelligent platform helps students and placement officers make data-driven decisions 
about campus placements using AI-powered resume matching.

### 📊 What We Offer:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 👨‍🎓 For Students
    - **Company-Based Matching**: Select companies that visited last year
    - **AI-Powered Analysis**: Get ATS and Semantic similarity scores
    - **Skill Gap Analysis**: Identify missing skills for your target role
    - **Personalized Recommendations**: Get course suggestions to improve
    """)
    
with col2:
    st.markdown("""
    ### 🏢 For Placement Unit
    - **Student Rankings**: Rank all applicants for a specific company
    - **Comparative Analysis**: See how students stack up against each other
    - **Data Export**: Download rankings as CSV for records
    - **Placement Insights**: Based on 2025 batch placement data
    """)

st.divider()

# Statistics
st.markdown("## 📈 Placement Statistics (2025 Batch)")

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

# How to Use
st.markdown("""
## 🚀 How to Get Started

### For Students:
1. Navigate to **👨‍🎓 Student Mode** from the sidebar
2. Select a company that visited last year
3. Choose the specific job role
4. Upload your resume (PDF format)
5. Click **Analyze Resume** to get your match score and recommendations

### For Placement Officers:
1. Navigate to **🏢 Placement Unit Mode** from the sidebar
2. Select a company and job role
3. Students can upload their resumes for that role
4. View real-time rankings of all applicants
5. Export data for placement records

""")

st.divider()

# Footer
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>Built with ❤️ using Streamlit, S-BERT, and NLTK</p>
    <p><small>Smart Hiring System v2.0 | Integrated with SCT Placement Data 2025</small></p>
</div>
""", unsafe_allow_html=True)

# Sidebar information
st.sidebar.success("Select a mode above to get started! 👆")
st.sidebar.info("""
### 💡 Quick Tip
Make sure your resume is in **PDF format** and contains relevant keywords 
for better matching results.
""")
