import langchain_helper as lch
import streamlit as st
import time

if 'processing' not in st.session_state:
  st.session_state.processing = False
if 'feedback_given' not in st.session_state:
  st.session_state.feedback_given = False

image_path = '/Users/canseluzun/Desktop/Consent-Guardian/CG-Logo.png'
st.image(image_path, width=300) 
st.title("Your shield in the digital realm!")
st.subheader("Where fairness meets privacy...")
  
action_type = st.sidebar.selectbox("What could Consent Guardian do to help you today?", ("Summarize", "On a scale of 1-10 Rate", "Answer Questions About"))

if action_type == "On a scale of 1-10 Rate":
  user_input = st.sidebar.text_area(
    label="What would you want your document to be rated for?",
    max_chars=30
    )

if action_type == "Answer Questions About":
  user_input = st.sidebar.text_area(
    label="What would you like to know about this document?",
    max_chars=100
    )
  
if action_type == "Summarize":
  user_input = st.sidebar.selectbox("Type of Summary?", ("Long", "Brief"))

with st.sidebar:
  openai_api_key = st.text_input("OpenAI API Key", type="password")
  "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

uploaded_file = st.file_uploader("Upload your document", type=['txt', 'pdf', 'docx'])
if uploaded_file is not None:
  document_content = uploaded_file.read().decode("utf-8")

  if st.button('Process') and openai_api_key:
      st.session_state.processing = True
      st.session_state.feedback_given = False

  if st.session_state.processing and not st.session_state.feedback_given:
    progress_bar = st.progress(0)
    for percentage_completed in range(100):
        time.sleep(0.05)
        progress_bar.progress(percentage_completed + 1)
    response = lch.process_document(action_type, user_input, openai_api_key, document_content)
    st.success("Document processed successfully!")
    st.markdown("## Analysis Results")
    st.text_area("#### Uploaded Document:", value=document_content, height=200)
    st.text_area("#### Response:", value=response.get("response", ""), height=200)

    st.markdown("#### Feedback")
    if st.button('👍'):
      st.session_state.feedback_given = True
      st.info("Thank you for your feedback!")
    if st.button('👎'):
      st.session_state.feedback_given = True
      st.session_state.processing = False  
      st.info("Please wait while we are improving your results!")
      improved_response = lch.process_document(action_type, user_input, openai_api_key, document_content)
      st.success("Document reprocessed successfully!")
      st.markdown("#### Improved Analysis Results")
      st.text_area("Improved Response:", value=improved_response.get("response", ""), height=200)
  else:
    st.info("Please add your OpenAI API key and a document to continue.")
else:
  st.warning("Please upload a document.")


  
  