import numpy as np
from PIL import Image

from .model import model
from .preprocess import preprocess


def predict(image: Image) -> np.ndarray:
    preprocessed_image = preprocess(image)
    predictions = model.predict(preprocessed_image)
    return predictions
