FROM python:3.8
RUN pip install -r requirements-flask.txt
COPY flask/health_check.py /app/health_check.py
WORKDIR /app
EXPOSE 8502
CMD ["python", "health_check.py"]
