import numpy as np
from keras.applications import resnet50
from keras.preprocessing.image import img_to_array
from PIL import Image


def preprocess(image: Image) -> np.ndarray:
    image = image.resize((224, 224))
    image = image.convert("RGB")
    numpy_image = img_to_array(image)
    image_batch = np.expand_dims(numpy_image, axis=0)
    processed_image = resnet50.preprocess_input(image_batch.copy())
    return processed_image
