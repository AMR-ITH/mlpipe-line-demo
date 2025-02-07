FROM python:3.13

WORKDIR /app

COPY flask_app/ /app/

COPY models/vectorizer.pkl /app/models/

RUN pip install -r /app/requirements.txt

RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000

# Set the command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]


# """ Muilti stage """

# # Stage 1: Build Stage
# FROM python:3.13 AS build

# WORKDIR /app

# # Copy the requirements.txt file from the flask_app folder
# COPY flask_app/requirements.txt /app/

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application code and model files
# COPY flask_app/ /app/
# COPY models/vectorizer.pkl /app/models/vectorizer.pkl

# # Download only the necessary NLTK data
# RUN python -m nltk.downloader stopwords wordnet

# # Stage 2: Final Stage
# FROM python:3.13-slim AS final

# WORKDIR /app

# # Copy only the necessary files from the build stage
# COPY --from=build /app /app

# # Expose the application port
# EXPOSE 5000

# # Set the command to run the application
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]