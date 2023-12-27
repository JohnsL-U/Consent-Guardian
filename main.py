import langchain_helper as lch
import streamlit as st
import time
import pypdf
from bs4 import BeautifulSoup
import base64
import utilities as utl
import streamlit.components.v1 as components


st.set_page_config(
	page_icon='CG-Logo.png', 
	layout="wide",
	page_title='Consent Guardian',
	initial_sidebar_state="expanded"
)

def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return "data:image/png;base64," + encoded

image_path = 'CG-Logo.png'
base64_image = get_image_base64(image_path)

html_content = f"""
<div class="header" style="text-align: center;">
    <figure>
      <img src="{base64_image}" alt="Logo" style="height: 200px;" />
      <h1>Welcome to Consent Guardian!</h1>
    </figure>
    <h3>Your shield in the digital realm!</h3>
</div>
"""

st.markdown(html_content, unsafe_allow_html=True)

def load_css():
  #Function to load CSS.
  utl.local_css("styles.css")
  utl.remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
  utl.remote_css('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700&display=swap')

load_css()

# Function to read different document types
def read_pdf(file):
  reader = pypdf.PdfReader(file)
  text = ""
  for page in range(len(reader.pages)):
      text += reader.pages[page].extract_text() + "\n"
  return text

def read_html(file):
  soup = BeautifulSoup(file, 'html.parser')
  return soup.get_text()

def run_streamlit_app():

  if 'processing' not in st.session_state:
    st.session_state.processing = False
  if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = False
  if 'initial_response' not in st.session_state:
    st.session_state.initial_response = None


  # Ask for the OpenAI API key
  openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
  if not openai_api_key:
      st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

  with st.expander("How to use 🦾", expanded=False):

    st.markdown(
      """
      Please refer to [our dedicated guide](https://github.com/JohnsL-U/Consent-Guardian/blob/main/README.md).
      """
      )

  # Chatbot Interface
  st.markdown("## 🤖 Guardian Chatbot")
  chatbot_query = st.text_input("Ask me anything about the document:")
  if st.button("Ask Guardian"):
      if 'uploaded_document' in st.session_state:
          # Process the chatbot query
          chatbot_response = lch.process_chatbot_query(chatbot_query, st.session_state.uploaded_document, openai_api_key)
          st.text_area("Chatbot Response:", value=chatbot_response, height=100)
      else:
          st.warning("Please upload a document first.")

  uploaded_file = st.sidebar.file_uploader("Upload your document", type=['txt', 'pdf', 'docx'])
  document_content = None
  if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
      document_content = read_pdf(uploaded_file)
    elif uploaded_file.type == "text/html":
      document_content = read_html(uploaded_file.getvalue().decode("utf-8"))
    else:
      document_content = uploaded_file.read().decode("utf-8")

    # Update session state with the uploaded document
    st.session_state.uploaded_document = document_content

  # Select the type of summary needed for the legal document
  summary_type = st.sidebar.selectbox("Select the type of summary you need for your document:", ("Executive Summary", "Key Points", "Detailed Analysis"))

  # Process Button
  if st.sidebar.button('Process') and openai_api_key and document_content:
      st.session_state.processing = True
      st.session_state.feedback_given = False
      progress_bar = st.progress(0)
      for percentage_completed in range(100):
          time.sleep(0.05)
          progress_bar.progress(percentage_completed + 1)
      response = lch.process_document(summary_type, openai_api_key, document_content)
      st.session_state.initial_response = response.get("response", "")
      st.success("Document processed successfully!")
      st.markdown("## Analysis Results")
      st.text_area("#### Uploaded Document:", value=document_content, height=200)
      st.text_area("#### Response:", value=st.session_state.initial_response, height=200)


  # Sidebar - Feedback Section
  if st.session_state.processing and not st.session_state.feedback_given:
    st.sidebar.markdown("### Feedback")
    if st.sidebar.button('👍'):
        st.sidebar.info("Thank you for your feedback!")

    elif st.sidebar.button('👎'):
        improved_response = lch.process_document(summary_type, openai_api_key, document_content, feedback='negative', initial_response=st.session_state.initial_response)
        # Store improved results and display in the main section
        if 'improved_response' in locals():
            st.session_state.improved_results = improved_response.get("response", "")
            st.success("Document reprocessed successfully!")
            st.text_area("### Improved Analysis Results", value=st.session_state.improved_results, height=200)

  # Additional UI Elements
  if not document_content:
      st.warning("Please upload a document.")
  elif not openai_api_key:
      st.warning("Please add your OpenAI API key to continue.")


if __name__ == "__main__":
  run_streamlit_app()
