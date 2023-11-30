import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv

load_dotenv()

def process_document(action_type, user_input, openai_api_key, document):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    prompt_template_name = PromptTemplate(
        input_variables = ['action_type','user_input'],
        template="I'm looking for assistance with a {document}. Please {action_type} it, considering the following aspect: {user_input}."
    )
    chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="response" )
    result = chain({'action_type': action_type, 'user_input': user_input, 'document':document})
    return result
