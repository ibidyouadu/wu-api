from PIL import Image
from io import BytesIO
import base64
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

def load_image(contents):
    """
    Given a base64 decoded image from a POST request to /result, return a tensorflow tensor
    representation of the image data.

    Parameters
    ----------
    contents : bytes
        Output from UploadFile.read()
    
    Returns
    -------
    image : tf.Tensor
        Tensor representation of the image data
    """
    bytes_image = BytesIO(contents)

    # Load image as batch tensor
    # https://www.tensorflow.org/api_docs/python/tf/keras/utils/load_img
    pil_image = keras.utils.load_img(bytes_image)
    array_image = keras.utils.img_to_array(pil_image)
    image = tf.convert_to_tensor(array_image)

    return image

def preprocess_image(image):
    """
    Normalize pixel values, reshape image if necessary, and convert to greyscale.
    """
    # Normalize pixel values
    image = image/255
    image = tf.cast(image,  tf.float32)

    # Reshape
    if image.shape != (400, 400, 3):
        image = tf.image.resize(image, [400, 400])

    # Convert to greyscale
    image = tf.tensordot(image, tf.constant([0.299, 0.587, 0.114]), axes=[[2], [0]])
    # grey_image = tf.expand_dims(grey_image, -1)

    return image