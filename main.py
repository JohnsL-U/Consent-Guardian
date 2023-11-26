import langchain_helper as lch
import streamlit as st

image_path = '/Users/canseluzun/Desktop/Consent-Guardian/static/CG-Logo.png'
st.image(image_path, width=300) 
st.title("Your shield in the digital realm!")
st.subheader("Where fairness meets privacy...")

uploaded_file = st.file_uploader("Upload your document", type=['txt', 'pdf', 'docx'])
if uploaded_file is not None and st.button('Process'):
    # To read file as string:
    stringio = uploaded_file.read().decode("utf-8")
    st.write("Document is being processed...")
else:
    st.warning("Please upload a document first.")

action_type = st.sidebar.selectbox("What could Consent Guardian do to help you today?", ("Summarize", "Rate", "Answer Questions About"))

if action_type == "Rate":
  user_input = st.sidebar.text_area(
    label="What would you want your document to be rated on a scale of 1-10?",
    max_chars=30
    )

if action_type == "Answer Questions About":
  user_input = st.sidebar.text_area(
    label="What would you like to know about this document?",
    max_chars=100
    )
  
if action_type == "Summarize":
  user_input = st.sidebar.selectbox("Type of Summary?", ("Detailed", "Brief"))

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

if user_input:
    if not openai_api_key:
      st.info("Please add your OpenAI API key to continue.")
      st.stop()
    response = lch.process_document(action_type, user_input, openai_api_key)
    st.write(response['response'])
    