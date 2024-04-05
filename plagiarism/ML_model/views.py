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

# def preprocess_text(text):
#     text = text.lower()
#     text = text.translate(str.maketrans('', '', string.punctuation))
#     tokens = word_tokenize(text)
#     stop_words = set(stopwords.words('english'))
#     filtered_tokens = [word for word in tokens if word not in stop_words]
#     # Join the filtered tokens back into text
#     preprocessed_text = ' '.join(filtered_tokens)
#     return preprocessed_text

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

def read_input(input_data):
    if isinstance(input_data, str):
        # If input is text content
        return input_data
    elif isinstance(input_data, bytes):
        # If input is PDF file content
        pdf_text = ''
        with fitz.open(stream=input_data, filetype="pdf") as pdf_file:
            for page_num in range(len(pdf_file)):
                page = pdf_file[page_num]
                pdf_text += page.get_text()
        return pdf_text
    else:
        raise ValueError("Unsupported input format. Please provide text content as a string or a PDF file as bytes.")

def detect_plagiarism(preprocessed_content):

    # Vectorize the preprocessed student document using the saved vectorizer
    X_student = vectorizer.transform([preprocessed_content])

    # Predict the plagiarism amount using the saved Random Forest model
    plagiarism_amount = random_forest_model.predict(X_student)[0]

    return plagiarism_amount

def automatic_grading(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    student_document_path = submission.submitted_file.path
    print(student_document_path)
    
   
    
    student_pdf_bytes = open(student_document_path, "rb").read()

    content_read = read_input(student_pdf_bytes)


    # Preprocess the student document
    preprocessed_student_text = preprocess_text2(content_read)

    # Detect plagiarism by passing the preprocessed text to detect_plagiarism function
    plagiarism_amount = detect_plagiarism(preprocessed_student_text)

    predicted_plagiarism = int(plagiarism_amount*100)
    print("Predicted amount of plagiarism detected: {}%".format(predicted_plagiarism))
    threshold=60
    if predicted_plagiarism>threshold:
        is_plagiarised = True
        print("The document is plagiarised!")
    else:
        is_plagiarised = False
        print("The document is not plagiarised")

    grade=0
    
    if is_plagiarised:
      return print("Grade:",grade)
    else:
      assignment = submission.assignment
      answer_key_path = assignment.pdf.path
      answer_key_pdf_bytes = open(student_document_path, "rb").read()
      answer_key = read_input(answer_key_pdf_bytes)

      max_grade=10

      # Preprocess the answer key
      preprocessed_answer_key_text = preprocess_text_grade(answer_key)

      # Preprocess the student document
      preprocessed_student_text_grade = preprocess_text_grade(content_read)

      vectorizer = TfidfVectorizer()
      tfidf_matrix = vectorizer.fit_transform([preprocessed_student_text_grade, preprocessed_answer_key_text])

      similarity_score = cosine_similarity(tfidf_matrix)[0, 1]
      grade = int(similarity_score*max_grade)
      print("Grade:",grade)
      return grade