from .vector_db import VectorDB
from pathlib import Path

class Retriever:
    def __init__(self, data_dir="rag_system/data/help_center", embeddings_dir="rag_system/data/embeddings"):
        self.db = VectorDB()
        
        # Cargar o construir índice
        if Path(embeddings_dir).exists() and list(Path(embeddings_dir).glob("*")):
            self.db.load_index(embeddings_dir)
        else:
            self.db.load_documents(data_dir)
            self.db.build_index()
            self.db.save_index(embeddings_dir)
    
    def get_relevant_documents(self, query, k=5):  # Aumentar resultados iniciales
        """Búsqueda semántica mejorada"""
        # Preprocesar query para mejor matching
        processed_query = f"{query} lemon"  # Añadir contexto de dominio
        
        results = self.db.search(processed_query, k=k)
        return sorted(results, key=lambda x: x['score'], reverse=True)