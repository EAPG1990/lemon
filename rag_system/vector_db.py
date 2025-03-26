import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorDB:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        self.index = None
        self.documents = []
        
    def load_documents(self, data_dir):
        """Carga documentos de diferentes formatos"""
        docs = []
        
        # Cargar archivos JSON
        for json_file in Path(data_dir).glob('*.json'):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    docs.extend(data)
        
        # Cargar archivos HTML (simplificado)
        for html_file in Path(data_dir).glob('*.html'):
            with open(html_file, 'r', encoding='utf-8') as f:
                docs.append({
                    'id': f"html-{html_file.stem}",
                    'title': html_file.stem,
                    'content': self._extract_text_from_html(f.read()),
                    'url': f"https://help.lemon.me/es/{html_file.stem}"
                })
        
        self.documents = docs
    
    def _extract_text_from_html(self, html):
        """Extrae texto básico de HTML (simplificado)"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
    
    def build_index(self):
        """Construye el índice FAISS"""
        if not self.documents:
            raise ValueError("No hay documentos cargados")
        
        # Generar embeddings
        texts = [f"{doc['title']}\n{doc['content']}" for doc in self.documents]
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        # embeddings = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        
        # Crear índice FAISS
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
    
    def save_index(self, save_dir):
        """Guarda el índice y metadatos"""
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        
        # Guardar índice FAISS
        faiss.write_index(self.index, str(Path(save_dir) / "index.faiss"))
        
        # Guardar metadatos
        with open(Path(save_dir) / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(self.documents, f)
    
    def load_index(self, save_dir):
        """Carga un índice existente"""
        self.index = faiss.read_index(str(Path(save_dir) / "index.faiss"))
        
        with open(Path(save_dir) / "metadata.json", 'r', encoding='utf-8') as f:
            self.documents = json.load(f)
    
    def search(self, query, k=3):
        """Busca documentos relevantes"""
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, score in zip(indices[0], distances[0]):
            if idx >= 0:  # FAISS puede devolver índices negativos
                doc = self.documents[idx]
                results.append({
                    'content': doc['content'],
                    'title': doc['title'],
                    'url': doc.get('url', ''),
                    'score': float(score)
                })
        
        return results