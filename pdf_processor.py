# pdf_processor.py
import PyPDF2
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF, or an empty string if an error occurs.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or "" # Handle cases where page.extract_text() might return None
    except PyPDF2.errors.PdfReadError:
        print(f"Error reading PDF file: {pdf_path}. It might be corrupted or encrypted.")
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {pdf_path}: {e}")
    return text

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
            print(extracted_text[:500]) # Print first 500 characters
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