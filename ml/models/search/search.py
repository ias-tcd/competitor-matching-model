from typing import List

import numpy as np

from .load import load
from .mappy import load as map_load


def search(embedding: np.ndarray) -> List[str]:
    tree = load("/src/ml/models/search/tree.h5")
    k = 4
    distances, indices = tree.search(embedding, k)
    brands_map = map_load()

    brands = [""] * k

    for name, brands_index in brands_map.items():
        for i, index in enumerate(indices.flatten()):
            if index in brands_index:
                brands[i] = name

    return brands
