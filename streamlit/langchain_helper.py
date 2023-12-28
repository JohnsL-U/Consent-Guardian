from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def process_document(summary_type, openai_api_key, document, feedback=None, initial_response=None):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    prompt_template_initial = PromptTemplate(
        input_variables = ['summary_type','document'],
        template="I'm looking for assistance with a {document}. Please provide a {summary_type}."
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
        result = chain_initial({'summary_type': summary_type, 'document': document})

    return result

def process_chatbot_query(query, document, openai_api_key):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    prompt = f"Based on the following document: {document}\n\nUser Query: {query}\n\nResponse:"
    response = llm(prompt)
    return response