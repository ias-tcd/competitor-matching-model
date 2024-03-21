from typing import Optional

from keras.applications.resnet50 import ResNet50
from keras.models import Model

model: Optional[Model] = None


def get_model() -> Model:
    global model

    if model:
        return model
    base_model = ResNet50(weights=None)
    base_model.load_weights("/src/ml/models/logo_recognition/resnet50.h5")

    second_last_layer = base_model.layers[-2].output

    model = Model(inputs=base_model.input, outputs=second_last_layer)

    return model
