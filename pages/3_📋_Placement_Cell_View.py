# pages/3_📋_Placement_Cell_View.py
import streamlit as st
from database import get_active_announcements, get_active_rankings
import pandas as pd

st.title("📋 Placement Cell - Announcements & Results")

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
st.write("View official announcements and published rankings from the Placement Cell.")
st.write("---")

# Create tabs
tab1, tab2 = st.tabs(["📢 Announcements", "🏆 Published Rankings"])

# ============ TAB 1: ANNOUNCEMENTS ============
with tab1:
    st.subheader("📢 Official Announcements")
    
    announcements = get_active_announcements()
    
    if announcements:
        for announcement in announcements:
            with st.expander(f"📣 {announcement['title']} - {announcement['created_at'][:10]}", expanded=True):
                st.write(f"**Posted by:** {announcement['posted_by_name']}")
                st.write(f"**Date:** {announcement['created_at'][:16]}")
                st.write("")
                st.success(announcement['message'])
    else:
        st.info("📭 No announcements at this time.")

# ============ TAB 2: PUBLISHED RANKINGS ============
with tab2:
    st.subheader("🏆 Published Rankings & Results")
    
    rankings = get_active_rankings()
    
    if rankings:
        for ranking in rankings:
            with st.expander(f"🏢 {ranking['title']} - {ranking['created_at'][:10]}", expanded=False):
                st.write(f"**Company:** {ranking['company_name']}")
                st.write(f"**Job Role:** {ranking['job_role']}")
                st.write(f"**Published by:** {ranking['published_by_name']}")
                st.write(f"**Date:** {ranking['created_at'][:16]}")
                
                if ranking['description']:
                    st.info(f"**Note:** {ranking['description']}")
                
                st.write("")
                st.write("**📊 Student Rankings:**")
                
                # Show rankings table
                rankings_list = ranking['rankings']
                
                # Check if current student is in the list
                student_rank = None
                for r in rankings_list:
                    if r['student_email'] == student_email:
                        student_rank = r
                        break
                
                if student_rank:
                    st.success(f"🎉 **Your Rank: {student_rank['rank']}** | Score: {student_rank['combined_score']:.1f}%")
                
                # Show full rankings
                df_data = []
                for r in rankings_list:
                    # Anonymize other students' emails
                    if r['student_email'] == student_email:
                        email_display = "You ⭐"
                    else:
                        email_display = r['student_email'][:3] + "***@" + r['student_email'].split('@')[1]
                    
                    df_data.append({
                        'Rank': r['rank'],
                        'Student': email_display,
                        'Combined Score': f"{r['combined_score']:.1f}%",
                        'ATS Score': f"{r['ats_score']:.1f}%",
                        'Semantic Score': f"{r['semantic_score']:.1f}%"
                    })
                
                st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
    else:
        st.info("📭 No rankings published yet.")
