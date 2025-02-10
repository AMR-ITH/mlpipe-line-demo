# FROM python:3.13

# WORKDIR /app

# COPY flask_app/ /app/

# COPY models/vectorizer.pkl /app/models/

# RUN pip install -r /app/requirements.txt

# RUN python -m nltk.downloader stopwords wordnet

# EXPOSE 5000

# # Set the command to run the application
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]


# """ Muilti stage """

# Stage 1: Build Stage
FROM python:3.13 AS build

WORKDIR /app

# Copy requirements and install dependencies
COPY flask_app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model files
COPY flask_app/ /app/
COPY models/vectorizer.pkl /app/models/vectorizer.pkl

# Download necessary NLTK data
RUN python -m nltk.downloader stopwords wordnet


# Stage 2: Final Stage
FROM python:3.13-slim AS final

WORKDIR /app

# Copy application files from build stage
COPY --from=build /app /app

# Install dependencies again in the final stage
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader stopwords wordnet

# Expose the application port
EXPOSE 5000

# Set the command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]