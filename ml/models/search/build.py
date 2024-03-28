import os
import pickle  # nosec
from typing import Dict

import faiss

from .load import load as load_tree
from .mappy import load, save
from .store import store


def build_pickles():
    directory = os.listdir("centroids")

    try:
        index = load_tree("/src/ml/models/search/tree.h5")
    except Exception as e:
        print(f"{e}")
        index = faiss.IndexFlatL2(2048)

    brands_map = load()
    count = find_max(brands_map) + 1

    for dir in directory:
        counts = []
        for file in os.listdir(f"centroids/{dir}"):
            with open(f"centroids/{dir}/{file}", "rb") as pickle_file:
                vector = pickle.load(pickle_file)  # nosec
            vector = vector.reshape((1, 2048))
            index.add(vector)
            counts.append(count)
            count += 1

        if dir in brands_map:
            brands_map[dir].extend(counts)
        else:
            brands_map[dir] = counts
    save(brands_map)
    store("/src/ml/models/search/tree.h5", index)


def find_max(brands_map: Dict) -> int:
    indices = []
    for v in brands_map.values():
        indices += v
    if len(indices) == 0:
        return -1
    return max(indices)
