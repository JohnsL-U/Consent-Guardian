from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import os

load_dotenv()

app = Flask(__name__)

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI LLM with your API key
llm = OpenAI(api_key=openai_api_key, temperature=0.7)

def process_document(document):
    prompt_template = PromptTemplate(
        input_variables=['document'],
        template="Summarize and rate the {document} for fairness and data privacy (1-10): Output must have Summary: and Rating: only"
    )
    
    # Split the document into segments of 1000 words each
    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain({'document': document})
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'document' not in request.files:
        return jsonify({'error': 'No document uploaded'}), 400
    document = request.files['document'].read().decode('utf-8')
    generated_text = process_document(document)
    
    summary_text = generated_text['text']
    if 'Rating:' in summary_text:
        # Split summary and rating
        parts = summary_text.split('Rating:')
        summary = parts[0].replace('Summary:', '').strip()
        rating = parts[1].strip()
    else:
        rating = "No rating found."
        summary = summary_text

    return render_template('results.html', rating=rating, summary=summary)


if __name__ == '__main__':
    app.run(debug=True, port=5003)

    

