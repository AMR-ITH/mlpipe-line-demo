FROM python:3.13

WORKDIR /app

COPY flask_app/ /app/

COPY models/vectorizer.pkl /app/models/

RUN pip install -r /app/requirements.txt

RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000

CMD ["python", "app.py"]