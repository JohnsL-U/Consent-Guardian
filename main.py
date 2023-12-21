import langchain_helper as lch
import streamlit as st
import time
import PyPDF2
from bs4 import BeautifulSoup
import io

if 'processing' not in st.session_state:
  st.session_state.processing = False
if 'feedback_given' not in st.session_state:
  st.session_state.feedback_given = False
if 'initial_response' not in st.session_state:
  st.session_state.initial_response = None

image_path = 'https://private-user-images.githubusercontent.com/93824716/281902819-365092b7-f5ab-4807-ac91-043bda15d158.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDE5MTAwODUsIm5iZiI6MTcwMTkwOTc4NSwicGF0aCI6Ii85MzgyNDcxNi8yODE5MDI4MTktMzY1MDkyYjctZjVhYi00ODA3LWFjOTEtMDQzYmRhMTVkMTU4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjA3VDAwNDMwNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQ0ODFiNzQ0NTQ1MmM0NzgyYjZkNjFiN2Q2ZDdkZDdhOWE4MjkxMGU2ZTQ2YmQ2OTJmYzBiMDFiYWUzOWNjZDImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.IS7dOH8ed-z1SNehga-9wuKCSiO2whqHR6yO7mosKyk'
st.image(image_path, width=300) 
st.title("Your shield in the digital realm!")
st.subheader("Where fairness meets privacy...")
  
action_type = st.sidebar.selectbox("What could Consent Guardian do to help you today?", ("Summarize", "On a scale of 1-10 Rate", "Answer Questions About"))
user_input = st.sidebar.text_area("Enter your specific requirements:", max_chars=100)

openai_api_key = ""
if action_type != "Summarize":
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if openai_api_key:
        st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

# Function to read different document types
def read_pdf(file):
  reader = PyPDF2.PdfReader(file)
  text = ""
  for page in range(len(reader.pages)):
      text += reader.pages[page].extract_text() + "\n"
  return text

def read_html(file):
  soup = BeautifulSoup(file, 'html.parser')
  return soup.get_text()

uploaded_file = st.file_uploader("Upload your document", type=['txt', 'pdf', 'docx'])
document_content = None
if uploaded_file is not None:
  if uploaded_file.type == "application/pdf":
    document_content = read_pdf(uploaded_file)
  elif uploaded_file.type == "text/html":
    document_content = read_html(uploaded_file.getvalue().decode("utf-8"))
  else:
    document_content = uploaded_file.read().decode("utf-8")

# Process Button
if st.button('Process') and ((action_type == "Summarize") or (action_type != "Summarize" and openai_api_key)) and document_content:
    st.session_state.processing = True
    st.session_state.feedback_given = False
    progress_bar = st.progress(0)
    for percentage_completed in range(100):
        time.sleep(0.05)
        progress_bar.progress(percentage_completed + 1)
    response = lch.process_document(action_type, user_input, openai_api_key, document_content)
    st.session_state.initial_response = response.get("response", "")
    st.success("Document processed successfully!")
    st.markdown("## Analysis Results")
    st.text_area("#### Uploaded Document:", value=document_content, height=200)
    st.text_area("#### Response:", value=st.session_state.initial_response, height=200)

# Feedback and Reprocessing Logic
if st.session_state.processing and not st.session_state.feedback_given:
    st.markdown("#### Feedback")
    if st.button('👍'):
        st.session_state.feedback_given = True
        st.info("Thank you for your feedback!")
    elif st.button('👎'):
        st.session_state.feedback_given = True
        st.session_state.processing = False  
        st.info("Please wait while we are improving your results!")
        improved_response = lch.process_document(action_type, user_input, openai_api_key, document_content, feedback='negative', initial_response=st.session_state.initial_response)
        st.success("Document reprocessed successfully!")
        st.markdown("#### Improved Analysis Results")
        st.text_area(value=improved_response.get("response", ""), height=200)

# Additional UI Elements
if not document_content:
    st.warning("Please upload a document.")
elif not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

