import os
import pickle
from typing import Dict

import faiss

from .load import load as load_tree
from .mappy import load, save
from .store import store


def build_pickles():
    directory = os.listdir("pickles")

    try:
        index = load_tree("/src/ml/models/search/tree.h5")
    except:
        index = faiss.IndexFlatL2(2048)

    brands_map = load()
    count = find_max(brands_map) + 1

    for dir in directory:
        counts = []
        for file in os.listdir(f"pickles/{dir}"):
            with open(f"pickles/{dir}/{file}", "rb") as pickle_file:
                vector = pickle.load(pickle_file)
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
        return 0
    return max(indices)
