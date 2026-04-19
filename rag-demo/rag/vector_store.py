import os
import faiss
import numpy as np
import pickle

class VectorStore:
    def __init__(self, dim=768):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        arr = np.array(embeddings)
    
        print("embedding shape:", arr.shape)  # ⭐关键调试
    
        if len(arr.shape) != 2:
            raise ValueError(f"embedding必须是二维数组，现在是: {arr.shape}")
    
        self.index.add(arr.astype('float32'))
        self.texts.extend(texts)
    
    def search(self, query_embedding, k=3):
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), k)
        return [self.texts[i] for i in I[0]]

    def save(self, path):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, path + "/index.faiss")
        with open(path + "/texts.pkl", "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, path):
        self.index = faiss.read_index(path + "/index.faiss")
        with open(path + "/texts.pkl", "rb") as f:
            self.texts = pickle.load(f)