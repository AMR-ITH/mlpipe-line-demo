from flask import Flask,render_template,request
import mlflow
from  preprocessing_utility import normalize_text
import pandas as pd
import pickle
import dagshub

mlflow.set_tracking_uri('https://dagshub.com/AMR-ITH/mlpipe-line-demo.mlflow')
dagshub.init(repo_owner='AMR-ITH', repo_name='mlpipe-line-demo', mlflow=True)

app = Flask(__name__)

# load model from model registry
model_name= "bow_model"
model_version= 1

model_uri = f"models:/{model_name}/{model_version}"
model = mlflow.pyfunc.load_model(model_uri)

# load vectorizer   
vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
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
    print(result[0])

    # show
    return result[0]

app.run(debug=True)