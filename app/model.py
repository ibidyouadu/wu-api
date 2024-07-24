from huggingface_hub import hf_hub_download
from tensorflow import keras
from params import MODEL_REPO_ID, MODEL_FILENAME
def get_model():
    """
    Download and load the model from huggingface
    """
    model_path = hf_hub_download(repo_id=MODEL_REPO_ID, filename=MODEL_FILENAME)
    model = keras.models.load_model(model_path)

    return model