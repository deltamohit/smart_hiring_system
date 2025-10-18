# Home.py
import streamlit as st
import nltk

# Download NLTK data on first run
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

# Rest of your existing Home.py code continues below...
# main.py
import os
from pdf_processor import extract_text_from_pdf, create_dummy_pdf
from text_preprocessor import preprocess_text
from data_manager import JOB_SKILL_DATABASE
from matcher import match_resume_to_job

def process_resume_from_pdf(pdf_path):
    """
    Extracts text from a PDF resume and then preprocesses it.
    """
    raw_text = extract_text_from_pdf(pdf_path)
    if raw_text:
        processed_text = preprocess_text(raw_text)
        return processed_text
    return ""

if __name__ == "__main__":
    print("=" * 60)
    print("SMART HIRING SYSTEM - TESTING PHASE")
    print("=" * 60)
    
    # Create a dummy PDF for testing
    dummy_pdf_content = """Software Engineer with 3 years of experience in Python development and machine learning.
Skills include Python, Java, SQL, Data Structures, Algorithms, Cloud Computing (AWS), Web Development.
Completed projects in data analysis and automated testing.
Seeking a challenging software engineering role."""
    
    dummy_pdf_path = os.path.join("data", "sample_resume_for_test.pdf")
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    print("\n[1/3] Creating and processing sample resume...")
    try:
        create_dummy_pdf(dummy_pdf_path, dummy_pdf_content)
        print(f"✓ Created dummy PDF at: {dummy_pdf_path}")
        
        processed_resume_text = process_resume_from_pdf(dummy_pdf_path)
        
        if processed_resume_text:
            print(f"✓ Successfully extracted and preprocessed resume")
            print(f"   Processed text preview: {processed_resume_text[:100]}...")
        else:
            print("✗ Failed to process the sample resume.")
            exit(1)
    
    except Exception as e:
        print(f"✗ An error occurred: {e}")
        exit(1)
    
    print("\n[2/3] Matching resume against job roles...")
    
    # Test matching for Software Engineer role
    test_job_role = "Software Engineer"
    print(f"\n--- Matching for: {test_job_role} ---")
    
    matching_result = match_resume_to_job(processed_resume_text, test_job_role)
    
    print(f"\n📊 MATCHING RESULTS:")
    print(f"   ATS Score (Keyword Match): {matching_result['ats_score']}%")
    print(f"   Semantic Similarity Score: {matching_result['semantic_score']}%")
    print(f"   Combined Score: {matching_result['combined_score']}%")
    
    print(f"\n✓ Matched Skills ({len(matching_result['matched_skills'])}/{matching_result['total_skills']}):")
    for skill in matching_result['matched_skills'][:10]:  # Show first 10
        print(f"   • {skill}")
    
    print(f"\n✗ Missing Skills ({len(matching_result['missing_skills'])}):")
    for skill in matching_result['missing_skills'][:5]:  # Show first 5
        print(f"   • {skill}")
    
    print(f"\n💡 PERSONALIZED FEEDBACK (Top 3 recommendations):")
    count = 0
    for skill, course in matching_result['feedback'].items():
        if count >= 3:
            break
        print(f"   {count+1}. {skill}: {course}")
        count += 1
    
    print("\n[3/3] Cleaning up...")
    if os.path.exists(dummy_pdf_path):
        os.remove(dummy_pdf_path)
        print(f"✓ Cleaned up {dummy_pdf_path}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext step: Run the Streamlit app with 'streamlit run app.py'")
