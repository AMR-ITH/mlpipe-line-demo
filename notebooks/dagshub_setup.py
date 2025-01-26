import dagshub
import mlflow

mlflow.set_tracking_uri('https://dagshub.com/AMR-ITH/mlpipe-line-demo.mlflow')
dagshub.init(repo_owner='AMR-ITH', repo_name='mlpipe-line-demo', mlflow=True)


with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)