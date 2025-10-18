# text_preprocessor.py
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

# Initialize NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def preprocess_text(text):
    """
    Applies a series of text preprocessing steps:
    1. Lowercasing
    2. Removing special characters and numbers
    3. Tokenization
    4. Stop word removal
    5. Lemmatization
    6. Stemming (optional, can be commented out if only lemmatization is desired)

    Args:
        text (str): The raw input text (e.g., extracted from a resume or JD).

    Returns:
        str: The processed text, joined back into a single string.
    """
    if not isinstance(text, str):
        return "" # Return empty string for non-string input

    # 1. Lowercasing
    text = text.lower()

    # 2. Remove special characters and numbers (keeping only alphabetic characters)
    # This also removes extra spaces
    text = re.sub(r'[^a-z\s]', '', text)

    # 3. Tokenization
    tokens = word_tokenize(text)

    # 4. Stop word removal
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # 5. Lemmatization
    lemmas = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # 6. Stemming (as per the paper, applying after lemmatization)
    # Stemming is a more aggressive reduction. You might choose only lemmatization
    # depending on desired semantic precision vs. reduction. The paper uses both.
    stemmed_words = [stemmer.stem(word) for word in lemmas]

    # Join the processed words back into a single string
    return " ".join(stemmed_words)

if __name__ == "__main__":
    print("--- Testing Text Preprocessing ---")

    sample_resume_text = """
    Experienced Software Developer with a strong background in Python, Java, and Machine Learning.
    My previous experience includes developing innovative solutions and performing data analysis.
    I love coding and continuously learning new technologies.
    Certifications: AWS, Azure. Looking for a challenging role in software engineering.
    """

    sample_jd_text = """
    We are seeking a highly motivated Software Engineer to join our dynamic team.
    The ideal candidate will have expertise in Python, data analysis, and cloud platforms like AWS.
    Experience in developing scalable applications is essential.
    Skills: Python, Java, SQL, Cloud Computing, Machine Learning.
    """

    print("\nOriginal Resume Text:")
    print(sample_resume_text)
    print("\nProcessed Resume Text:")
    processed_resume = preprocess_text(sample_resume_text)
    print(processed_resume)

    print("\nOriginal Job Description Text:")
    print(sample_jd_text)
    print("\nProcessed Job Description Text:")
    processed_jd = preprocess_text(sample_jd_text)
    print(processed_jd)

    # Example with non-string input
    print("\nTesting with non-string input:")
    print(preprocess_text(None))
    print(preprocess_text(123))