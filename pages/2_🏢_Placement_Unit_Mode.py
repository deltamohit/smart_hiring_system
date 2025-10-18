# pages/2_🏢_Placement_Unit_Mode.py
import streamlit as st
import pandas as pd
import os
import tempfile
from datetime import datetime
from pdf_processor import extract_text_from_pdf
from text_preprocessor import preprocess_text
from matcher import match_resume_to_job
from company_database import COMPANY_JOB_SKILLS
from data_manager import JOB_SKILL_DATABASE

# Page Configuration
st.set_page_config(
    page_title="Placement Unit Mode - Smart Hiring",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Placement Unit Mode: Student Rankings")
st.markdown("View and rank all students who uploaded resumes for a specific company and role.")

st.divider()

# Initialize session state for storing student data
if 'student_submissions' not in st.session_state:
    st.session_state.student_submissions = []

# Get list of companies
companies = sorted(COMPANY_JOB_SKILLS.keys())

# Sidebar - Company and Role Selection
st.sidebar.header("🎯 Select Company & Role")

selected_company = st.sidebar.selectbox(
    "Choose Company:",
    options=companies,
    key="placement_company"
)

# Get job roles for selected company
if selected_company:
    job_roles = list(COMPANY_JOB_SKILLS[selected_company].keys())
    
    selected_role = st.sidebar.selectbox(
        "Choose Job Role:",
        options=job_roles,
        key="placement_role"
    )
    
    # Display selected job info
    st.sidebar.markdown(f"### 📌 Selected Position")
    st.sidebar.info(f"**Company:** {selected_company}\n\n**Role:** {selected_role}")
    
    # Required skills
    required_skills = COMPANY_JOB_SKILLS[selected_company][selected_role]
    
    st.sidebar.divider()
    
    # Clear data button
    if st.sidebar.button("🗑️ Clear All Submissions", type="secondary"):
        st.session_state.student_submissions = []
        st.sidebar.success("All submissions cleared!")
        st.rerun()

st.divider()

# Two columns layout
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📤 Upload Student Resume")
    st.markdown("Upload resumes one by one to add them to the ranking system.")
    
    # Student name input
    student_name = st.text_input("Student Name:", placeholder="Enter student name")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=['pdf'],
        key="placement_upload"
    )
    
    if uploaded_file and student_name:
        if st.button("➕ Add to Ranking", type="primary", use_container_width=True):
            with st.spinner(f"Processing {student_name}'s resume..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_file_path = tmp_file.name
                    
                    # Extract and preprocess text
                    raw_text = extract_text_from_pdf(tmp_file_path)
                    
                    if raw_text and len(raw_text.strip()) > 0:
                        processed_text = preprocess_text(raw_text)
                        
                        if processed_text and len(processed_text.strip()) > 0:
                            # Create temporary job key for matching
                            temp_job_key = f"{selected_company} - {selected_role}"
                            JOB_SKILL_DATABASE[temp_job_key] = required_skills
                            
                            # Perform matching
                            result = match_resume_to_job(processed_text, temp_job_key)
                            
                            # Check if student already exists
                            existing = [s for s in st.session_state.student_submissions 
                                      if s['name'] == student_name and 
                                      s['company'] == selected_company and 
                                      s['role'] == selected_role]
                            
                            if existing:
                                st.warning(f"⚠️ {student_name} has already submitted for this role. Updating scores...")
                                # Remove old entry
                                st.session_state.student_submissions = [
                                    s for s in st.session_state.student_submissions 
                                    if not (s['name'] == student_name and 
                                           s['company'] == selected_company and 
                                           s['role'] == selected_role)
                                ]
                            
                            # Add student data
                            student_data = {
                                'name': student_name,
                                'company': selected_company,
                                'role': selected_role,
                                'ats_score': result['ats_score'],
                                'semantic_score': result['semantic_score'],
                                'combined_score': result['combined_score'],
                                'matched_skills': len(result['matched_skills']),
                                'missing_skills': len(result['missing_skills']),
                                'total_skills': result['total_skills'],
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            st.session_state.student_submissions.append(student_data)
                            st.success(f"✅ {student_name}'s resume added successfully!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Resume appears empty after processing.")
                    else:
                        st.error("❌ Could not extract text from PDF.")
                    
                    # Clean up
                    os.unlink(tmp_file_path)
                
                except Exception as e:
                    st.error(f"❌ Error processing resume: {str(e)}")
    
    elif uploaded_file and not student_name:
        st.warning("⚠️ Please enter student name before uploading.")

with col2:
    st.header("📊 Student Rankings")
    
    # Filter submissions for current company and role
    filtered_submissions = [
        s for s in st.session_state.student_submissions
        if s['company'] == selected_company and s['role'] == selected_role
    ]
    
    if filtered_submissions:
        # Sort by combined score (descending)
        sorted_students = sorted(filtered_submissions, key=lambda x: x['combined_score'], reverse=True)
        
        # Display summary metrics
        st.markdown(f"### 📈 Summary Statistics")
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.metric("Total Applicants", len(sorted_students))
        
        with col_b:
            avg_score = sum(s['combined_score'] for s in sorted_students) / len(sorted_students)
            st.metric("Average Score", f"{avg_score:.1f}%")
        
        with col_c:
            st.metric("Highest Score", f"{sorted_students[0]['combined_score']}%")
        
        with col_d:
            st.metric("Lowest Score", f"{sorted_students[-1]['combined_score']}%")
        
        st.divider()
        
        # Create DataFrame for display
        df = pd.DataFrame(sorted_students)
        df['rank'] = range(1, len(df) + 1)
        
        # Reorder columns
        display_df = df[['rank', 'name', 'combined_score', 'ats_score', 'semantic_score', 
                         'matched_skills', 'missing_skills', 'total_skills', 'timestamp']]
        
        display_df.columns = ['Rank', 'Student Name', 'Overall Score (%)', 'ATS Score (%)', 
                             'Semantic Score (%)', 'Skills Matched', 'Skills Missing', 
                             'Total Skills', 'Submission Time']
        
        # Display table with color coding
        st.markdown("### 🏆 Detailed Rankings")
        
        # Add color coding function
        def highlight_scores(val):
            if isinstance(val, (int, float)):
                if val >= 70:
                    return 'background-color: #d4edda'  # Green
                elif val >= 50:
                    return 'background-color: #fff3cd'  # Yellow
                else:
                    return 'background-color: #f8d7da'  # Red
            return ''
        
        # Apply styling
        styled_df = display_df.style.applymap(
            highlight_scores, 
            subset=['Overall Score (%)', 'ATS Score (%)', 'Semantic Score (%)']
        )
        
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        st.divider()
        
        # Download options
        st.markdown("### 💾 Export Data")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # CSV download
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Rankings as CSV",
                data=csv,
                file_name=f"{selected_company}_{selected_role}_rankings_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_export2:
            # Excel download
            excel_buffer = pd.ExcelWriter('temp_rankings.xlsx', engine='openpyxl')
            display_df.to_excel(excel_buffer, index=False, sheet_name='Rankings')
            excel_buffer.close()
            
            with open('temp_rankings.xlsx', 'rb') as f:
                st.download_button(
                    label="📥 Download Rankings as Excel",
                    data=f,
                    file_name=f"{selected_company}_{selected_role}_rankings_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            # Clean up temp file
            if os.path.exists('temp_rankings.xlsx'):
                os.remove('temp_rankings.xlsx')
        
        st.divider()
        
        # Top performers section
        st.markdown("### 🌟 Top 5 Performers")
        
        top_5 = sorted_students[:5]
        for idx, student in enumerate(top_5, 1):
            with st.expander(f"#{idx} - {student['name']} ({student['combined_score']}%)"):
                col_detail1, col_detail2 = st.columns(2)
                
                with col_detail1:
                    st.markdown(f"""
                    **Overall Score:** {student['combined_score']}%  
                    **ATS Score:** {student['ats_score']}%  
                    **Semantic Score:** {student['semantic_score']}%
                    """)
                
                with col_detail2:
                    st.markdown(f"""
                    **Skills Matched:** {student['matched_skills']}/{student['total_skills']}  
                    **Skills Missing:** {student['missing_skills']}  
                    **Submitted:** {student['timestamp']}
                    """)
    
    else:
        st.info("👈 No submissions yet. Upload student resumes to start ranking.")
        st.markdown("""
        ### 📝 How to Use:
        1. Enter student name in the left panel
        2. Upload their resume (PDF)
        3. Click "Add to Ranking"
        4. Repeat for all students
        5. View rankings and export data
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 10px;'>
    <p><small>🏢 Placement Unit Dashboard | Data is session-based and will reset on page reload</small></p>
</div>
""", unsafe_allow_html=True)
