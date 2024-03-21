import faiss

def store(filename, index):
    faiss.write_index(index, filename)
