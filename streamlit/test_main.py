import main
from main import read_pdf, read_html
import io
from langchain_helper import process_document, process_chatbot_query
from unittest import mock
from unittest.mock import patch
from io import BytesIO
from reportlab.pdfgen import canvas
import pytest
from unittest.mock import Mock

class MockLLMChain:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        # Check if 'feedback' is in kwargs and is negative
        if kwargs.get('feedback') == 'negative':
            return {'refined_response': 'Mocked refined summary response'}
        else:
            return {'response': 'Mocked summary response'}

class MockOpenAI:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return 'Mocked chatbot response'

@pytest.fixture
def mock_llm_chain(mocker):
    mocker.patch('langchain_helper.LLMChain', new=MockLLMChain)

@pytest.fixture
def mock_openai(mocker):
    mocker.patch('langchain_helper.OpenAI', new=MockOpenAI)

def test_process_document_without_feedback(mock_llm_chain):
    # Test data
    test_summary_type = 'Executive Summary'
    test_document = 'Sample document content'
    test_openai_api_key = 'test_key'

    # Call the function
    result = process_document(test_summary_type, test_openai_api_key, test_document)

    # Assert the expected response
    assert result == {'response': 'Mocked summary response'}

def test_process_document_with_feedback(mock_llm_chain):
    # Test data
    test_summary_type = 'Executive Summary'
    test_document = 'Sample document content'
    test_openai_api_key = 'test_key'
    test_initial_response = 'Initial response'
    
    # Call the function with negative feedback
    result = process_document(test_summary_type, test_openai_api_key, test_document, feedback='negative', initial_response=test_initial_response)

    # Assert the expected response
    assert result == {'response': 'Mocked summary response'}


def test_process_chatbot_query(mock_openai):
    # Test data
    test_query = 'Sample query'
    test_document = 'Sample document content'
    test_openai_api_key = 'test_key'

    # Call the function
    result = process_chatbot_query(test_query, test_document, test_openai_api_key)

    # Assert the expected response
    assert result == 'Mocked chatbot response'

def test_read_html():
    mock_html_content = '<p>Mock HTML Content</p>'
    mock_html = io.BytesIO(mock_html_content.encode('utf-8'))
    assert read_html(mock_html) == 'Mock HTML Content'

# Function to create a mock PDF file
def create_mock_pdf(content):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, content)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def test_read_pdf():
    mock_pdf_content = "Mock PDF Content"
    mock_pdf = create_mock_pdf(mock_pdf_content)
    actual_content = read_pdf(mock_pdf)
    expected_content = mock_pdf_content
    assert expected_content in actual_content


def test_api_key_input():
    # Mock the Streamlit UI input for the API key
    with mock.patch('main.st') as mock_st:
        mock_st.sidebar.text_input.return_value = 'mock_api_key'
        main.openai_api_key = mock_st.sidebar.text_input("OpenAI API Key")
        assert main.openai_api_key == 'mock_api_key'

def test_integration():
    # Mock the langchain_helper's process_document function
    with mock.patch('langchain_helper.process_document') as mock_process_document:
        mock_process_document.return_value = {'response': 'Mock response'}

        # Simulate the Streamlit button click
        with mock.patch('main.st') as mock_st:
            mock_st.button.return_value = True
            main.run_streamlit_app() 

            # Check if process_document was called
            mock_process_document.assert_called_once()