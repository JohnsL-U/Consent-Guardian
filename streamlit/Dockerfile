FROM python:3.8
RUN pip install -r requirements.txt
COPY streamlit/main.py /app/main.py
WORKDIR /app
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]









