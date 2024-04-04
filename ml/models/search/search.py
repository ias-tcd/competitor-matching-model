import logging
from typing import List, Tuple

import numpy as np

from .load import load
from .mappy import load as map_load

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def search_and_distances(embedding: np.ndarray) -> Tuple[List[str], List]:
    tree = load("/src/ml/models/search/tree.h5")
    k = 4
    distances_and_indices = tree.search(embedding, k)
    distances, indices = filter_(*distances_and_indices)
    brands_map = map_load()

    brands = [""] * k

    for name, brands_index in brands_map.items():
        for i, index in enumerate(indices.flatten()):
            if index in brands_index:
                brands[i] = name

    logger.info(f"Brands detected: {brands} with distances {distances} and indices {indices}")

    return brands, distances


def search(embedding: np.ndarray) -> List[str]:
    brands, _ = search_and_distances(embedding)
    return brands


def filter_(distances, indices):
    filtered_distances = []
    filtered_indices = []
    for distance, index in zip(distances[0], indices[0]):
        if distance <= 1200:
            filtered_distances.append(distance)
            filtered_indices.append(index)

    return filtered_distances, np.array(filtered_indices)
