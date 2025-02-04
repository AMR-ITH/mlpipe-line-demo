from flask import Flask,render_template,request
import mlflow
from  preprocessing_utility import normalize_text
import pandas as pd
import pickle
import os

import dagshub



dagshub_token = os.getenv("DAGSHUB_PAT")
if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

repo_owner = "AMR-ITH"
repo_name = "mlpipe-line-demo"
dagshub_url = f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"

# Set the MLflow tracking URI to the DagsHub tracking server
mlflow.set_tracking_uri(dagshub_url)

app = Flask(__name__)

# load model from model registry

def load_model_with_fallback(model_name: str, alias: str = "deployment"):
    """Load a model from the MLflow Model Registry using an alias, with a fallback to the latest version."""
    client = mlflow.MlflowClient()
    try:
        # Construct the model URI using the alias
        model_uri = f"models:/{model_name}@{alias}"
        # Attempt to load the model using the alias
        model = mlflow.pyfunc.load_model(model_uri)
        print(f"Model loaded using alias '{alias}'.")
    except mlflow.MlflowException as e:
        print(f"Alias '{alias}' not found. Fetching the latest version based on model name.")
        # Get the latest version information for the model
        latest_versions = client.get_latest_versions(model_name)
        # Extract the version number of the latest version
        latest_version_number = latest_versions[0].version
        # Construct the model URI using the latest version number
        model_uri = f"models:/{model_name}/{latest_version_number}"
        # Load the model using the latest version number
        model = mlflow.pyfunc.load_model(model_uri)
        print(f"Model loaded using the latest version: {latest_version_number}.")
    return model

model_name = "bow_model_github_actions"
model = load_model_with_fallback(model_name)

# load vectorizer   
vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    text = request.form['text']

    # clean
    text = normalize_text(text)

    # bow
    features = vectorizer.transform([text])

    # Convert sparse matrix to DataFrame
    features_df = pd.DataFrame.sparse.from_spmatrix(features)
    features_df = pd.DataFrame(features.toarray(), columns=[str(i) for i in range(features.shape[1])])

    # prediction
    result = model.predict(features_df)

    # show
    return render_template('index.html', result=result[0])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")