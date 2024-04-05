from django.shortcuts import redirect,render
import joblib
from pprint import PrettyPrinter
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import joblib
import fitz  # PyMuPDF
import tempfile
from django.contrib import messages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import nltk
nltk.download('wordnet')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

random_forest_vectorizer = joblib.load('ML_model/Model/vectorizer_random_forest2.pkl')
random_forest_model = joblib.load('ML_model/Model/random_forest_model2.pkl')

def preprocess_text2(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Join the filtered tokens back into text
    preprocessed_text2 = ' '.join(filtered_tokens)
    return preprocessed_text2

def check(request):
     if request.method == 'POST' and request.FILES.get('pdf_file'):
        # Get the PDF file
        pdf_file = request.FILES['pdf_file']
        print("got pdf")
        
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in pdf_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name   
            
        # Read text content from the temporary file
        pdf_text = ''
        with fitz.open(temp_file_path) as pdf_document:
            for page in pdf_document:
                pdf_text += page.get_text()
                    
        print("extracted")  
        # Preprocess the student document
        preprocessed_student_text = preprocess_text2(pdf_text)

        # Vectorize the preprocessed student document using the saved vectorizer
        X_student = random_forest_vectorizer.transform([preprocessed_student_text])

        # Predict the plagiarism amount using the saved Random Forest model
        plagiarism_amount = random_forest_model.predict(X_student)[0]
        result = plagiarism_amount * 100

        is_plagiarized = result > 40
        
        return result, is_plagiarized
     else:
        return None,None


def read_input(input_data):
    pdf_text = ''
    with fitz.open(stream=input_data, filetype="pdf") as pdf_file:
        for page_num in range(len(pdf_file)):
            page = pdf_file[page_num]
            pdf_text += page.get_text()
    return pdf_text
    
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Join the filtered tokens back into text
    preprocessed_text = ' '.join(filtered_tokens)
    return preprocessed_text

def preprocess_text_grade(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [token.translate(table) for token in tokens]
    stop_words = set(stopwords.words('english'))
    words = [word for word in stripped if word not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word) for word in words]

    # Join the lemmatized words back into a single string
    preprocessed_text = ' '.join(lemmas)

    return preprocessed_text

# Function to detect plagiarism
def detect_plagiarism(preprocessed_content):

    # Vectorize the preprocessed student document using the saved vectorizer
    X_student = random_forest_vectorizer.transform([preprocessed_content])

    # Predict the plagiarism amount using the saved Random Forest model
    plagiarism_amount = random_forest_model.predict(X_student)[0]

    return plagiarism_amount

