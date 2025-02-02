import os
import mlflow

def promote_model():
    """Promote a model version to a specified stage in the MLflow Model Registry."""
    # Set up DagsHub credentials for MLflow tracking
    dagshub_token = os.getenv("DAGSHUB_PAT")
    if not dagshub_token:
        raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = "AMR-ITH"
    repo_name = "mlpipe-line-demo"

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    client = mlflow.tracking.MlflowClient()
    # Get the latest version with the 'staging' alias

    model_name = "bow_model_github_actions"
    model_version_info = client.get_model_version_by_alias(model_name, "staging")
    # Set the new alias 'deployment' for the same version
    client.set_registered_model_alias(
        name=model_name,
        alias="deployment",
        version=model_version_info.version
    )

    # Add a tag to the model version
    client.set_model_version_tag(
        name=model_name,
        version=model_version_info.version,
        key="deployment_status",
        value="deployed"
    )

if __name__ == "__main__":
    promote_model()