import numpy as np
from PIL import Image

from .model import get_model
from .preprocess import preprocess


def predict(image: Image) -> np.ndarray:
    model = get_model()
    preprocessed_image = preprocess(image)
    predictions = model.predict(preprocessed_image)
    return predictions
