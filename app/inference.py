from datasets import load_dataset
from tensorflow import keras
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder
from params import DATASET_REPO_ID, label_names_to_english


def get_label_encoder():
    """
    Create LabelEncoder object to translate integers to text.
    """
    dataset_info = load_dataset(DATASET_REPO_ID, split="train", streaming=True)._info
    labels = dataset_info.features['label'].names
    labels = [label_names_to_english[l] for l in labels]
    le = LabelEncoder()
    le.fit(labels)

    return le

def make_prediction(model, input):
    """
    Make prediction for image and return the label and associated probability.

    Parameters
    ----------
    model : keras.Sequential
        The cloud identifier model
    input : tf.Tensor
        Output from preproceess_data()

    Returns
    -------
    predicted_label_name : str
        Name of the most likely label
    predicted_proba : np.float64
        Probability of the most likely label
    """
    batch = tf.expand_dims(input, axis=0)
    probabilities = model.predict(batch)
    predicted = np.argmax(probabilities)
    predicted_proba = round(np.max(probabilities) * 100, 1)

    le = get_label_encoder()
    predicted_label_name = le.inverse_transform(predicted.reshape(1,))[0]

    return predicted_label_name, predicted_proba