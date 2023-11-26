import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

from dotenv import load_dotenv

load_dotenv()

def process_document(action_type, user_input, api_key):
    llm =OpenAI(temperature=0.7)
    prompt_template_name = PromptTemplate(
        input_variables = ['action_type','user_input'],
        template="I'm looking for assistance with a document. Please {action_type} it, considering the following aspect: {user_input}."
    )
    chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="response" )
    result = chain({'action_type': action_type, 'user_input': user_input})
    return result



