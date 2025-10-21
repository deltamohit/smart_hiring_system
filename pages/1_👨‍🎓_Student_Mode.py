# pages/1_👨‍🎓_Student_Mode.py
import streamlit as st
from pdf_processor import extract_text_from_pdf
from text_preprocessor import preprocess_text
from matcher import match_resume_to_job
from database import (
    save_student_resume, 
    get_current_resume, 
    get_all_resume_versions,
    save_analysis_result,
    get_student_analysis_history,
    get_company_specific_history
)
from datetime import datetime
import pandas as pd

st.title("👨‍🎓 Student Mode - Resume Analysis")

# Check authentication
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("⚠️ Please login first!")
    st.stop()

if st.session_state['user_type'] != 'student':
    st.error("❌ This page is only for students!")
    st.stop()

student_email = st.session_state['user_email']
student_name = st.session_state['user_name']

st.write(f"**Welcome, {student_name}!**")
st.write("---")

# ============ SECTION 1: CURRENT RESUME & UPLOAD ============

st.subheader("📄 Your Resume")

current_resume = get_current_resume(student_email)

col1, col2 = st.columns([2, 1])

with col1:
    if current_resume:
        st.success(f"✅ Current Resume: **{current_resume['resume_filename']}**")
        st.info(f"📅 Uploaded: {current_resume['uploaded_at'][:10]} | Version: {current_resume['version_number']}")
    else:
        st.info("📤 No resume uploaded yet. Please upload your resume below.")

with col2:
    if st.button("📂 View All Versions", use_container_width=True):
        st.session_state['show_versions'] = not st.session_state.get('show_versions', False)

# Show resume version history
if st.session_state.get('show_versions', False):
    st.write("#### 📚 Resume Version History")
    all_versions = get_all_resume_versions(student_email)
    
    if all_versions:
        version_data = []
        for v in all_versions:
            version_data.append({
                'Version': v['version_number'],
                'Filename': v['resume_filename'],
                'Uploaded': v['uploaded_at'][:10],
                'Status': '✅ Current' if v['is_current'] else '📋 Previous'
            })
        st.dataframe(pd.DataFrame(version_data), use_container_width=True, hide_index=True)
    else:
        st.info("No resume versions found.")

st.write("---")

# Upload new resume section
with st.expander("📤 Upload New Resume", expanded=not current_resume):
    st.write("Upload a new version of your resume. This will be saved as version " + 
             str(current_resume['version_number'] + 1 if current_resume else 1))
    
    uploaded_file = st.file_uploader("Choose your resume (PDF)", type=['pdf'], key='resume_upload')
    
    if uploaded_file and st.button("💾 Save Resume", use_container_width=True):
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            
            if resume_text and len(resume_text.strip()) > 50:
                result = save_student_resume(student_email, resume_text, uploaded_file.name)
                
                if result:
                    st.success(f"✅ Resume uploaded successfully as Version {result[0]['version_number']}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Error saving resume. Please try again.")
            else:
                st.error("❌ Could not extract text from PDF. Please ensure it's a valid resume.")

st.write("---")

# ============ SECTION 2: PREVIOUS INSIGHTS ============

st.subheader("📊 Your Previous Insights")

analysis_history = get_student_analysis_history(student_email)

if analysis_history:
    # Group by company
    companies = {}
    for analysis in analysis_history:
        company = analysis['company_name']
        if company not in companies:
            companies[company] = []
        companies[company].append(analysis)
    
    st.write(f"**Total Companies Analyzed: {len(companies)}**")
    
    # Show each company's insights
    for company, analyses in companies.items():
        with st.expander(f"🏢 {company} ({len(analyses)} analysis{'es' if len(analyses) > 1 else ''})"):
            for idx, analysis in enumerate(analyses):
                st.write(f"**Analysis #{idx + 1}** | 📅 {analysis['analyzed_at'][:16]} | 📄 Resume v{analysis['resume_version']}")
                st.write(f"**Job Role:** {analysis['job_role']}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("ATS Score", f"{analysis['ats_score']:.1f}%")
                col2.metric("Semantic", f"{analysis['semantic_score']:.1f}%")
                col3.metric("Combined", f"{analysis['combined_score']:.1f}%")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write("**✅ Matched Skills:**")
                    if analysis['matched_skills']:
                        for skill in analysis['matched_skills'][:5]:
                            st.write(f"• {skill}")
                        if len(analysis['matched_skills']) > 5:
                            st.write(f"*...and {len(analysis['matched_skills']) - 5} more*")
                
                with col_b:
                    st.write("**❌ Missing Skills:**")
                    if analysis['missing_skills']:
                        for skill in analysis['missing_skills'][:5]:
                            st.write(f"• {skill}")
                        if len(analysis['missing_skills']) > 5:
                            st.write(f"*...and {len(analysis['missing_skills']) - 5} more*")
                
                if idx < len(analyses) - 1:
                    st.write("---")
else:
    st.info("📭 No previous analyses yet. Analyze your resume below to get started!")

st.write("---")

# ============ SECTION 3: NEW ANALYSIS ============

st.subheader("🔍 Analyze Resume for Company")

if not current_resume:
    st.warning("⚠️ Please upload a resume first!")
    st.stop()

# Import from your company database
from company_database import COMPANY_JOB_SKILLS

# Company selection (dropdown with real companies)
company_name = st.selectbox("Select Company", sorted(list(COMPANY_JOB_SKILLS.keys())))

# Job role selection (based on selected company)
if company_name:
    available_roles = list(COMPANY_JOB_SKILLS[company_name].keys())
    job_role = st.selectbox("Select Job Role", available_roles)
    
    # Check for previous analysis
    previous_analysis = get_company_specific_history(student_email, company_name)
    
    if previous_analysis:
        st.info(f"💡 You have {len(previous_analysis)} previous analysis{'es' if len(previous_analysis) > 1 else ''} for {company_name}")
    
    if st.button("🚀 Analyze Resume", use_container_width=True, type="primary"):
        with st.spinner("Analyzing your resume..."):
            # Preprocess resume text
            processed_text = preprocess_text(current_resume['resume_text'])
            
            # Calculate scores using your matcher function
            results = match_resume_to_job(processed_text, company_name, job_role)
            
            # Check for errors
            if 'error' in results:
                st.error(f"❌ {results['error']}")
                st.stop()
            
            # Convert feedback dict to string for storage
            feedback_str = str(results['feedback'])
            
            # Save to database
            save_analysis_result(
                student_email=student_email,
                company_name=company_name,
                job_role=job_role,
                resume_version=current_resume['version_number'],
                resume_filename=current_resume['resume_filename'],
                ats_score=results['ats_score'],
                semantic_score=results['semantic_score'],
                combined_score=results['combined_score'],
                matched_skills=results['matched_skills'],
                missing_skills=results['missing_skills'],
                feedback=feedback_str
            )
            
            st.success("✅ Analysis complete and saved!")
            
            # Display results
            st.write("### 📈 Current Analysis Results")
            st.write(f"**Company:** {company_name} | **Role:** {job_role}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("ATS Score", f"{results['ats_score']:.1f}%")
            col2.metric("Semantic Score", f"{results['semantic_score']:.1f}%")
            col3.metric("Combined Score", f"{results['combined_score']:.1f}%")
            
            st.write("---")
            
            # Show comparison if previous analysis exists
            if len(previous_analysis) > 0:
                st.write("### 📊 Progress Comparison")
                
                latest_prev = previous_analysis[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📋 Previous Analysis**")
                    st.write(f"📅 Date: {latest_prev['analyzed_at'][:10]}")
                    st.write(f"📄 Resume Version: {latest_prev['resume_version']}")
                    st.metric("ATS", f"{latest_prev['ats_score']:.1f}%")
                    st.metric("Semantic", f"{latest_prev['semantic_score']:.1f}%")
                    st.metric("Combined", f"{latest_prev['combined_score']:.1f}%")
                
                with col2:
                    st.write("**✨ Current Analysis**")
                    st.write(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
                    st.write(f"📄 Resume Version: {current_resume['version_number']}")
                    
                    ats_diff = results['ats_score'] - latest_prev['ats_score']
                    sem_diff = results['semantic_score'] - latest_prev['semantic_score']
                    comb_diff = results['combined_score'] - latest_prev['combined_score']
                    
                    st.metric("ATS", f"{results['ats_score']:.1f}%", f"{ats_diff:+.1f}%")
                    st.metric("Semantic", f"{results['semantic_score']:.1f}%", f"{sem_diff:+.1f}%")
                    st.metric("Combined", f"{results['combined_score']:.1f}%", f"{comb_diff:+.1f}%")
                
                st.write("---")
                
                # Improvement feedback
                if comb_diff > 5:
                    st.success(f"🎉 **Excellent progress!** Your score improved by {comb_diff:.1f}%!")
                elif comb_diff > 0:
                    st.success(f"👍 **Good improvement!** Your score increased by {comb_diff:.1f}%")
                elif comb_diff < -5:
                    st.warning(f"📉 Score decreased by {abs(comb_diff):.1f}%. Review the missing skills.")
                elif comb_diff < 0:
                    st.info(f"📊 Small decrease of {abs(comb_diff):.1f}%.")
                else:
                    st.info("📊 Your score remained stable.")
                
                # Skills comparison
                st.write("#### 🔄 Skills Progress")
                
                new_skills = set(results['matched_skills']) - set(latest_prev['matched_skills'])
                lost_skills = set(latest_prev['matched_skills']) - set(results['matched_skills'])
                
                if new_skills:
                    st.success(f"**✨ New Skills Added ({len(new_skills)}):**")
                    for skill in new_skills:
                        st.write(f"• {skill}")
                
                if lost_skills:
                    st.warning(f"**⚠️ Skills No Longer Detected ({len(lost_skills)}):**")
                    for skill in lost_skills:
                        st.write(f"• {skill}")
                
                if not new_skills and not lost_skills:
                    st.info("No change in matched skills.")
            
            st.write("---")
            
            # Show matched and missing skills
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.write("**✅ Matched Skills:**")
                for skill in results['matched_skills']:
                    st.write(f"• {skill}")
                if not results['matched_skills']:
                    st.write("*No skills matched*")
            
            with col_b:
                st.write("**❌ Missing Skills to Add:**")
                if results['missing_skills']:
                    for skill in results['missing_skills']:
                      st.write(f"• **{skill}**")
                      if skill in results['feedback']:
                        st.info(f"📚 {results['feedback'][skill]}")
                else:
                    st.write("*You have all required skills!*")
           
