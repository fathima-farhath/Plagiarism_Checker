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

# Create your views here.
#SVM
# def preprocess_text(text):
#     text = text.lower()
#     text = text.translate(str.maketrans('', '', string.punctuation))
#     tokens = word_tokenize(text)
#     stop_words = set(stopwords.words('english'))
#     filtered_tokens = [word for word in tokens if word not in stop_words]
#     # Join the filtered tokens back into text
#     preprocessed_text = ' '.join(filtered_tokens)
#     return preprocessed_text

# vectorizer = joblib.load('ML_model/Model/vectorizer1.pkl')
# svm = joblib.load('ML_model/Model/svm_model1.pkl')

# def plagiarism_checker(request):
#     print(request.FILES)
#     if request.method == 'POST' and request.FILES.get('pdf_file'):
#         # Get the PDF file
#         pdf_file = request.FILES['pdf_file']
#         print("got pdf")
        
#         # Save the uploaded file to a temporary location
#         with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#             for chunk in pdf_file.chunks():
#                 temp_file.write(chunk)
#             temp_file_path = temp_file.name

#         # Read text content from the temporary file
#         pdf_text = ''
#         with fitz.open(temp_file_path) as pdf_document:
#             for page in pdf_document:
#                 pdf_text += page.get_text()
                
#         print("extracted")
#         # Preprocess the text content
#         preprocessed_content = preprocess_text(pdf_text)
#         print("preproccessed")

#         # Vectorize the preprocessed text using TF-IDF
#         X_uploaded = vectorizer.transform([preprocessed_content])

#         # Make predictions using the SVM model
#         y_pred_uploaded = svm.predict(X_uploaded)

#         # Output the predictions
#         if y_pred_uploaded[0] == 0:
#             #messages.success(request,'The document is not plagiarized')
#             result = "0"
#         else:
#             #messages.success(request,'The document is plagiarized')
#             result = "1"
#     else:
#         result = "2"
#         #messages.success(request,'No file uploaded')   
#     return render(request, 'dashboard/student/student.html', {'result': result})


#RANDOM FOREST
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

def plagiarism_checker2(request):
    print(request.FILES)
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
        #messages.success("Plagiarism amount= ",plagiarism_amount)
    else:
        result = "No file is found"  
    return render(request, 'dashboard/student/student.html', {'result': result})  