import faiss

def load(filename):
    index = faiss.read_index(filename)
    return index
