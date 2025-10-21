# pages/2_🏢_Placement_Unit_Mode.py
import streamlit as st
from database import (
    create_announcement, get_all_announcements, delete_announcement, toggle_announcement_status,
    publish_ranking, get_all_rankings, delete_ranking,
    get_all_student_analyses, get_student_by_email,
    save_student_resume, get_current_resume, save_analysis_result
)
from company_database import COMPANY_JOB_SKILLS
from datetime import datetime
import pandas as pd
import json

st.title("🏢 Placement Unit - Officer Dashboard")

# Check authentication
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("⚠️ Please login first!")
    st.stop()

if st.session_state['user_type'] != 'placement_cell':
    st.error("❌ This page is only for placement cell officers!")
    st.stop()

officer_email = st.session_state['user_email']
officer_name = st.session_state['user_name']

st.write(f"**Welcome, {officer_name}!**")
st.write("---")

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["📢 Announcements", "🏆 Rank Students", "📋 Manage Published Results"])

# ============ TAB 1: ANNOUNCEMENTS ============
with tab1:
    st.subheader("📢 Send Announcement to Students")
    
    with st.expander("✍️ Create New Announcement", expanded=True):
        with st.form("announcement_form", clear_on_submit=True):
            announcement_title = st.text_input(
                "Announcement Title*",
                placeholder="e.g., Infosys Drive on 25th Oct",
                max_chars=200
            )
            
            announcement_message = st.text_area(
                "Announcement Message*",
                placeholder="Enter detailed message for students...",
                height=150,
                max_chars=2000
            )
            
            submit_button = st.form_submit_button("📤 Send Announcement", type="primary")
            
            if submit_button:
                if not announcement_title or not announcement_message:
                    st.error("❌ Please fill both title and message!")
                else:
                    result = create_announcement(
                        title=announcement_title,
                        message=announcement_message,
                        posted_by_email=officer_email,
                        posted_by_name=officer_name
                    )
                    
                    if result:
                        st.success("✅ Announcement sent to all students!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to send announcement.")
    
    st.write("---")
    st.subheader("📋 Manage Announcements")
    
    all_announcements = get_all_announcements()
    
    if all_announcements:
        for announcement in all_announcements:
            status_icon = "✅" if announcement['is_active'] else "🚫"
            
            with st.expander(f"{status_icon} {announcement['title']} - {announcement['created_at'][:10]}"):
                st.write(f"**Posted by:** {announcement['posted_by_name']}")
                st.write(f"**Date:** {announcement['created_at'][:16]}")
                st.info(announcement['message'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if announcement['is_active']:
                        if st.button("🚫 Deactivate", key=f"deact_ann_{announcement['id']}"):
                            toggle_announcement_status(announcement['id'], False)
                            st.rerun()
                    else:
                        if st.button("✅ Activate", key=f"act_ann_{announcement['id']}"):
                            toggle_announcement_status(announcement['id'], True)
                            st.rerun()
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_ann_{announcement['id']}"):
                        delete_announcement(announcement['id'])
                        st.rerun()
    else:
        st.info("📭 No announcements yet.")

# ============ TAB 2: RANK STUDENTS ============
with tab2:
    st.subheader("🏆 Rank Students for Company")
    
    # Create sub-tabs for existing analyses and manual upload
    subtab1, subtab2 = st.tabs(["📊 Rank & Publish", "📤 Upload New Resumes"])
    
    # ===== SUBTAB 1: RANK EXISTING ANALYSES =====
    with subtab1:
        st.write("#### Rank all students (existing + manually uploaded)")
        
        # Select company and job role
        company_name = st.selectbox("Select Company", sorted(list(COMPANY_JOB_SKILLS.keys())), key="rank_company")
        
        if company_name:
            available_roles = list(COMPANY_JOB_SKILLS[company_name].keys())
            job_role = st.selectbox("Select Job Role", available_roles, key="rank_role")
            
            if st.button("🔍 Load Student Rankings", type="primary"):
                # Get all analyses for this company/role (LATEST per student only)
                student_analyses = get_all_student_analyses(company_name, job_role)
                
                if student_analyses:
                    st.success(f"✅ Found {len(student_analyses)} unique students for {company_name} - {job_role}")
                    st.info(f"💡 Showing latest analysis per student (duplicates removed)")
                    
                    # Create ranking dataframe
                    ranking_data = []
                    for idx, analysis in enumerate(student_analyses, 1):
                        # Get student details
                        student = get_student_by_email(analysis['student_email'])
                        student_name = student['name'] if student else "Unknown"
                        
                        ranking_data.append({
                            'Rank': idx,
                            'Student Name': student_name,
                            'Email': analysis['student_email'],
                            'Resume Ver.': analysis['resume_version'],
                            'Combined Score': f"{analysis['combined_score']:.1f}%",
                            'ATS': f"{analysis['ats_score']:.1f}%",
                            'Semantic': f"{analysis['semantic_score']:.1f}%",
                            'Date': analysis['analyzed_at'][:10]
                        })
                    
                    df = pd.DataFrame(ranking_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    st.write("---")
                    st.subheader("📤 Publish This Ranking")
                    
                    with st.form("publish_ranking_form"):
                        result_title = st.text_input(
                            "Result Title*",
                            value=f"{company_name} - {job_role} Rankings",
                            max_chars=200
                        )
                        
                        result_description = st.text_area(
                            "Description (Optional)",
                            placeholder="Add notes about this ranking...",
                            height=100
                        )
                        
                        publish_button = st.form_submit_button("📢 Publish Rankings to Students", type="primary")
                        
                        if publish_button:
                            if not result_title:
                                st.error("❌ Please enter a title!")
                            else:
                                # Convert to JSON-serializable format
                                rankings_json = [
                                    {
                                        'rank': item['Rank'],
                                        'student_name': item['Student Name'],
                                        'student_email': item['Email'],
                                        'combined_score': float(analysis['combined_score']),
                                        'ats_score': float(analysis['ats_score']),
                                        'semantic_score': float(analysis['semantic_score'])
                                    }
                                    for item, analysis in zip(ranking_data, student_analyses)
                                ]
                                
                                result = publish_ranking(
                                    title=result_title,
                                    company_name=company_name,
                                    job_role=job_role,
                                    description=result_description,
                                    rankings=rankings_json,
                                    published_by_email=officer_email,
                                    published_by_name=officer_name
                                )
                                
                                if result:
                                    st.success("✅ Rankings published! Students can now view them.")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to publish rankings.")
                else:
                    st.warning(f"⚠️ No students have analyzed their resume for {company_name} - {job_role} yet.")
                    st.info("💡 Use the 'Upload New Resumes' tab to manually add student resumes.")
    
    # ===== SUBTAB 2: MANUAL UPLOAD =====
    with subtab2:
        st.write("#### Manually upload and analyze student resumes")
        st.info("📌 Upload resumes for students who haven't uploaded yet. They will be merged with existing analyses.")
        
        # Select company and role
        company_name_manual = st.selectbox("Select Company", sorted(list(COMPANY_JOB_SKILLS.keys())), key="manual_company")
        
        if company_name_manual:
            available_roles_manual = list(COMPANY_JOB_SKILLS[company_name_manual].keys())
            job_role_manual = st.selectbox("Select Job Role", available_roles_manual, key="manual_role")
            
            # Show existing analyses count
            existing_analyses = get_all_student_analyses(company_name_manual, job_role_manual)
            st.info(f"ℹ️ Currently {len(existing_analyses)} student(s) have analyzed for this role")
            
            st.write("---")
            
            # Multiple resume upload
            uploaded_files = st.file_uploader(
                "Upload Student Resumes (PDF)",
                type=['pdf'],
                accept_multiple_files=True,
                key="manual_upload"
            )
            
            if uploaded_files:
                st.write(f"📄 {len(uploaded_files)} resume(s) uploaded")
                
                # Show preview
                with st.expander("👀 Preview Uploaded Files"):
                    for file in uploaded_files:
                        st.write(f"• {file.name}")
                
                if st.button("🚀 Analyze All Resumes", type="primary", key="analyze_manual"):
                    # Lazy import - only load when needed
                    from pdf_processor import extract_text_from_pdf
                    from text_preprocessor import preprocess_text
                    from matcher import match_resume_to_job
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results_list = []
                    
                    for idx, uploaded_file in enumerate(uploaded_files):
                        status_text.text(f"Analyzing {uploaded_file.name}...")
                        
                        # Extract and process
                        resume_text = extract_text_from_pdf(uploaded_file)
                        
                        if resume_text and len(resume_text.strip()) > 50:
                            processed_text = preprocess_text(resume_text)
                            
                            # Calculate scores
                            results = match_resume_to_job(processed_text, company_name_manual, job_role_manual)
                            
                            if 'error' not in results:
                                results['filename'] = uploaded_file.name
                                results['resume_text'] = resume_text
                                results_list.append(results)
                        
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    status_text.text("✅ Analysis complete!")
                    
                    if results_list:
                        st.success(f"✅ Successfully analyzed {len(results_list)} resume(s)!")
                        
                        # Show results
                        st.write("### 📊 Analysis Results")
                        
                        # Sort by combined score
                        results_list.sort(key=lambda x: x['combined_score'], reverse=True)
                        
                        preview_data = []
                        for idx, result in enumerate(results_list, 1):
                            preview_data.append({
                                'Rank': idx,
                                'File Name': result['filename'],
                                'Combined Score': f"{result['combined_score']:.1f}%",
                                'ATS Score': f"{result['ats_score']:.1f}%",
                                'Semantic Score': f"{result['semantic_score']:.1f}%"
                            })
                        
                        st.dataframe(pd.DataFrame(preview_data), use_container_width=True, hide_index=True)
                        
                        st.write("---")
                        st.write("### 📤 Assign to Students & Save")
                        st.warning("⚠️ Assign each resume to a registered student email to save the analysis.")
                        
                        # Create form to assign emails
                        with st.form("assign_emails_form"):
                            st.write("**Assign Student Emails:**")
                            
                            email_assignments = {}
                            for idx, result in enumerate(results_list):
                                email_assignments[idx] = st.text_input(
                                    f"{result['filename']}",
                                    placeholder="student@sctce.ac.in",
                                    key=f"email_{idx}"
                                )
                            
                            save_button = st.form_submit_button("💾 Save Analyses", type="primary")
                            
                            if save_button:
                                # Validate emails
                                valid = True
                                for idx, email in email_assignments.items():
                                    if not email or '@' not in email:
                                        st.error(f"❌ Invalid email for {results_list[idx]['filename']}")
                                        valid = False
                                        break
                                    
                                    # Check if student exists
                                    student = get_student_by_email(email)
                                    if not student:
                                        st.error(f"❌ Student with email {email} not found in database!")
                                        st.info(f"💡 Student must be registered first. Email: {email}")
                                        valid = False
                                        break
                                
                                if valid:
                                    # Save all analyses
                                    for idx, result in enumerate(results_list):
                                        student_email = email_assignments[idx]
                                        
                                        # Save resume first
                                        save_student_resume(
                                            student_email=student_email,
                                            resume_text=result['resume_text'],
                                            filename=result['filename']
                                        )
                                        
                                        # Get the resume version that was just saved
                                        current_resume = get_current_resume(student_email)
                                        
                                        # Save analysis
                                        save_analysis_result(
                                            student_email=student_email,
                                            company_name=company_name_manual,
                                            job_role=job_role_manual,
                                            resume_version=current_resume['version_number'],
                                            resume_filename=result['filename'],
                                            ats_score=result['ats_score'],
                                            semantic_score=result['semantic_score'],
                                            combined_score=result['combined_score'],
                                            matched_skills=result['matched_skills'],
                                            missing_skills=result['missing_skills'],
                                            feedback=str(result['feedback'])
                                        )
                                    
                                    st.success(f"✅ All {len(results_list)} resume(s) saved successfully!")
                                    st.info("💡 Go back to 'Rank & Publish' tab to see the updated rankings with newly added students.")
                                    st.balloons()
                    else:
                        st.error("❌ No valid resumes could be analyzed.")
            
            st.write("---")
            st.write("#### 🔄 After Uploading")
            st.info("""
            **Next Steps:**
            1. Save the manually uploaded resumes (assign student emails above)
            2. Go to **'Rank & Publish'** tab
            3. Click 'Load Student Rankings' to see ALL students (existing + newly uploaded)
            4. Publish the combined rankings
            """)

# ============ TAB 3: MANAGE PUBLISHED RESULTS ============
with tab3:
    st.subheader("📋 Manage Published Rankings")
    
    all_rankings = get_all_rankings()
    
    if all_rankings:
        st.write(f"**Total Published Rankings: {len(all_rankings)}**")
        
        for ranking in all_rankings:
            status_icon = "✅" if ranking['is_active'] else "🚫"
            
            with st.expander(f"{status_icon} {ranking['title']} - {ranking['created_at'][:10]}"):
                st.write(f"**Company:** {ranking['company_name']}")
                st.write(f"**Job Role:** {ranking['job_role']}")
                st.write(f"**Published by:** {ranking['published_by_name']}")
                st.write(f"**Date:** {ranking['created_at'][:16]}")
                
                if ranking['description']:
                    st.info(f"**Description:** {ranking['description']}")
                
                # Show top 5 rankings
                rankings_list = ranking['rankings']
                if rankings_list:
                    st.write(f"**Total Students Ranked:** {len(rankings_list)}")
                    
                    top_5 = rankings_list[:5]
                    df_data = []
                    for r in top_5:
                        df_data.append({
                            'Rank': r['rank'],
                            'Student': r['student_name'],
                            'Score': f"{r['combined_score']:.1f}%"
                        })
                    
                    st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
                
                if st.button("🗑️ Delete Ranking", key=f"del_rank_{ranking['id']}"):
                    delete_ranking(ranking['id'])
                    st.success("Ranking deleted!")
                    st.rerun()
    else:
        st.info("📭 No published rankings yet.")
