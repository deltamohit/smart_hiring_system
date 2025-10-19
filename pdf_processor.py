# pdf_processor.py
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Import PyPDF2 with fallback for different versions
try:
    from PyPDF2 import PdfReader
except ImportError:
    from PyPDF2 import PdfFileReader as PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from all pages
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def create_dummy_pdf(file_path, content):
    """Creates a simple PDF file for testing purposes."""
    c = canvas.Canvas(file_path, pagesize=letter)
    text_lines = content.strip().split('\n')
    y_position = 750
    for line in text_lines:
        c.drawString(100, y_position, line.strip())
        y_position -= 15
    c.save()


if __name__ == "__main__":
    # --- For Testing ---
    dummy_pdf_content = """
    This is a sample resume content.
    It contains various skills like Python, Java, SQL, and Machine Learning.
    Experience includes data analysis and software development.
    Looking for a challenging role.
    """
    dummy_pdf_path = os.path.join("data", "sample_resume.pdf")

    # Ensure 'data' directory exists
    os.makedirs('data', exist_ok=True)

    print("--- Testing PDF Text Extraction ---")
    try:
        create_dummy_pdf(dummy_pdf_path, dummy_pdf_content)
        print(f"Created a dummy PDF at: {dummy_pdf_path}")

        extracted_text = extract_text_from_pdf(dummy_pdf_path)
        if extracted_text:
            print("Successfully extracted text:")
            print("-" * 30)
            print(extracted_text[:500])
            print("-" * 30)
        else:
            print("Failed to extract any text from the dummy PDF.")
    except ImportError:
        print("ReportLab not installed. Skipping dummy PDF creation and extraction test.")
    except Exception as e:
        print(f"An error occurred during dummy PDF test: {e}")
    finally:
        if os.path.exists(dummy_pdf_path):
            os.remove(dummy_pdf_path)
            print(f"Cleaned up {dummy_pdf_path}")
