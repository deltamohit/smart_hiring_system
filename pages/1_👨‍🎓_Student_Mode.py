# pages/1_👨‍🎓_Student_Mode.py
import streamlit as st
import os
import tempfile
from pdf_processor import extract_text_from_pdf
from text_preprocessor import preprocess_text
from matcher import match_resume_to_job
from company_database import COMPANY_JOB_SKILLS, SKILL_COURSE_MAP

# Page Configuration
st.set_page_config(
    page_title="Student Mode - Smart Hiring",
    page_icon="👨‍🎓",
    layout="wide"
)

st.title("👨‍🎓 Student Mode: Resume Analysis")
st.markdown("Upload your resume and check your match percentage with companies that visited SCT last year!")

st.divider()

# Get list of companies
companies = sorted(COMPANY_JOB_SKILLS.keys())

# Sidebar - Company and Role Selection
st.sidebar.header("🎯 Select Target Company & Role")

selected_company = st.sidebar.selectbox(
    "Choose Company:",
    options=companies,
    help="Select from companies that visited SCT in 2024-2025"
)

# Get job roles for selected company
if selected_company:
    job_roles = list(COMPANY_JOB_SKILLS[selected_company].keys())
    
    selected_role = st.sidebar.selectbox(
        "Choose Job Role:",
        options=job_roles,
        help="Select the specific role you're targeting"
    )
    
    # Display selected job info
    st.sidebar.markdown(f"### 📌 Selected Position")
    st.sidebar.info(f"**Company:** {selected_company}\n\n**Role:** {selected_role}")
    
    # Display required skills
    st.sidebar.markdown("### 🔑 Key Required Skills")
    required_skills = COMPANY_JOB_SKILLS[selected_company][selected_role]
    for skill in required_skills[:8]:
        st.sidebar.markdown(f"• {skill}")
    if len(required_skills) > 8:
        st.sidebar.markdown(f"*...and {len(required_skills) - 8} more*")

st.divider()

# Main Content - File Upload
st.header("📤 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume (PDF format)",
    type=['pdf'],
    help="Upload your resume in PDF format for analysis"
)

if uploaded_file is not None:
    st.success(f"✅ File uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.2f} KB)")
    
    # Process button
    if st.button("🔍 Analyze My Resume", type="primary", use_container_width=True):
        with st.spinner("🤖 Analyzing your resume against the job requirements... This may take a few seconds..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                
                # Extract and preprocess text
                raw_text = extract_text_from_pdf(tmp_file_path)
                
                if not raw_text or len(raw_text.strip()) == 0:
                    st.error("❌ Could not extract text from the PDF. Please ensure it's a valid, non-encrypted PDF.")
                else:
                    processed_text = preprocess_text(raw_text)
                    
                    if not processed_text or len(processed_text.strip()) == 0:
                        st.error("❌ Resume appears to be empty after processing. Please check your resume content.")
                    else:
                        # Create a temporary job database entry for matching
                        from data_manager import JOB_SKILL_DATABASE
                        
                        # Add the selected company-role to the database temporarily
                        temp_job_key = f"{selected_company} - {selected_role}"
                        JOB_SKILL_DATABASE[temp_job_key] = required_skills
                        
                        # Perform matching
                        result = match_resume_to_job(processed_text, temp_job_key)
                        
                        # Display Results
                        st.success("✅ Analysis Complete!")
                        
                        # Scores Section
                        st.header("📊 Your Match Scores")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                label="ATS Score",
                                value=f"{result['ats_score']}%",
                                help="Keyword match percentage"
                            )
                        
                        with col2:
                            st.metric(
                                label="Semantic Score",
                                value=f"{result['semantic_score']}%",
                                help="AI-based contextual similarity"
                            )
                        
                        with col3:
                            st.metric(
                                label="Overall Match",
                                value=f"{result['combined_score']}%",
                                help="Combined match score",
                                delta=f"{result['combined_score'] - 50:.1f}% vs average"
                            )
                        
                        # Interpretation with color coding
                        if result['combined_score'] >= 70:
                            st.success("🎉 **Excellent Match!** Your resume is very well-aligned with this role. You have a strong chance!")
                        elif result['combined_score'] >= 50:
                            st.info("👍 **Good Match!** Your resume shows potential. Consider adding a few more relevant skills to boost your score.")
                        else:
                            st.warning("⚠️ **Room for Improvement!** Focus on building key skills for this role. Check the recommendations below.")
                        
                        st.divider()
                        
                        # Skills Breakdown
                        st.header("🎯 Detailed Skills Analysis")
                        
                        col_matched, col_missing = st.columns(2)
                        
                        with col_matched:
                            st.subheader(f"✅ Skills You Have ({len(result['matched_skills'])})")
                            if result['matched_skills']:
                                for skill in result['matched_skills']:
                                    st.markdown(f"✓ {skill}")
                            else:
                                st.markdown("*No matched skills found. Consider adding relevant keywords to your resume.*")
                        
                        with col_missing:
                            st.subheader(f"❌ Skills to Develop ({len(result['missing_skills'])})")
                            if result['missing_skills']:
                                for skill in result['missing_skills'][:12]:
                                    st.markdown(f"• {skill}")
                                if len(result['missing_skills']) > 12:
                                    st.markdown(f"*...and {len(result['missing_skills']) - 12} more*")
                            else:
                                st.markdown("*Great! You have all required skills!*")
                        
                        st.divider()
                        
                        # Personalized Feedback
                        if result['missing_skills']:
                            st.header("💡 Personalized Learning Path")
                            st.markdown("Here are recommended courses to help you build the missing skills:")
                            
                            # Create tabs for different categories if needed
                            recommendations = []
                            for skill in result['missing_skills'][:8]:  # Top 8 missing skills
                                if skill in SKILL_COURSE_MAP:
                                    recommendations.append((skill, SKILL_COURSE_MAP[skill]))
                                else:
                                    recommendations.append((skill, f"Search for '{skill}' courses on Coursera, Udemy, or edX"))
                            
                            for idx, (skill, course) in enumerate(recommendations, 1):
                                with st.expander(f"📚 {idx}. Learn {skill.capitalize()}"):
                                    st.markdown(f"**Recommended:** {course}")
                                    st.markdown(f"**Priority:** {'High' if idx <= 3 else 'Medium'}")
                        
                        st.divider()
                        
                        # Action Items
                        st.header("✅ Next Steps")
                        st.markdown(f"""
                        1. **Focus on top 3-5 missing skills** to maximize your match score
                        2. **Update your resume** with projects demonstrating these skills
                        3. **Re-analyze** your updated resume to track improvement
                        4. **Apply** when you reach 70%+ match score for best chances
                        """)
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
            
            except Exception as e:
                st.error(f"❌ An error occurred during analysis: {str(e)}")
                st.markdown("Please try again or contact the placement cell if the issue persists.")

else:
    st.info("👆 Please upload your resume PDF to begin analysis")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 10px;'>
    <p><small>💡 Tip: Make sure your resume includes relevant keywords, projects, and skills for better matching</small></p>
</div>
""", unsafe_allow_html=True)
