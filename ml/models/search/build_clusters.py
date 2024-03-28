import os
import pickle  # nosec
from typing import List

import numpy as np
from sklearn.cluster import KMeans

MAX_NUMBER_OF_CLUSTERS = 4
COMPANIES = ["adidas"]


def generate_clusters():
    os.makedirs("/src/centroids", exist_ok=True)
    for company in COMPANIES:
        _generate_clusters_for_company(company)


def _generate_clusters_for_company(company_name: str):
    vectors = _get_vectors_for_company(company_name)
    data = np.array(vectors)
    data = np.reshape(data, (data.shape[0], data.shape[2]))
    k_means_clusters = KMeans(n_clusters=MAX_NUMBER_OF_CLUSTERS, random_state=0)
    k_means_clusters.fit(data)
    centroids = k_means_clusters.cluster_centers_
    _save_centroids(company_name, centroids)


def _get_vectors_for_company(company_name: str) -> List[np.ndarray]:
    file_path = f"/src/pickles/{company_name}"
    vectors = []
    for file in os.listdir(file_path):
        if not file.endswith(".pkl"):
            continue
        pickle_path = os.path.join(file_path, file)
        with open(pickle_path, "rb") as pickle_file:
            vector = pickle.load(pickle_file)  # nosec
            vectors.append(vector)
    return vectors


def _save_centroids(company_name: str, centroids):
    path_name = f"/src/centroids/{company_name}"
    os.makedirs(path_name, exist_ok=True)
    for i, centroid in enumerate(centroids):
        with open(os.path.join(path_name, f"centroid_{i}.pkl"), "wb") as pickle_file:
            pickle.dump(centroid, pickle_file)
