import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import pipeline

hf_summarizer = pipeline("summarization")

def process_document(action_type, user_input, openai_api_key, document, feedback=None, initial_response=None):
    if action_type.lower() == "summarize":
        # Summarize the document using Hugging Face's Transformers
        summary = hf_summarizer(document, max_length=130, min_length=30, do_sample=False)
        return {'response': summary[0]['summary_text']}
    else:
        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
        prompt_template_initial = PromptTemplate(
            input_variables = ['action_type','user_input'],
            template="I'm looking for assistance with a {document}. Please {action_type} it, considering the following aspect: {user_input}."
        )
        chain_initial = LLMChain(llm=llm, prompt=prompt_template_initial, output_key="response" )

        # If feedback is provided and it's negative, process the document further
        if feedback and feedback == 'negative' and initial_response:
            prompt_template_feedback = PromptTemplate(
                input_variables=['response'],
                template="The initial response received negative feedback. Please refine or elaborate on this summary: {response}."
            )
            chain_feedback = LLMChain(llm=llm, prompt=prompt_template_feedback, output_key="refined_response")
            result = chain_feedback({'response': initial_response})
        else:
            result = chain_initial({'action_type': action_type, 'user_input': user_input, 'document': document})

    return result
