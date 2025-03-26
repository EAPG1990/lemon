from .retriever import Retriever
from .generator import AnswerGenerator

class RAGSystem:
    def __init__(self, use_simple_generator=False):
        self.retriever = Retriever()
        self.use_simple = use_simple_generator
        self.generator = AnswerGenerator()
    
    def query(self, question, max_sources=2, min_confidence=0.3):
        """Consulta mejorada con parámetros de filtrado"""
        # Paso 1: Recuperar documentos relevantes
        docs = self.retriever.get_relevant_documents(question)
        print(f"Scores de documentos: {[doc['score'] for doc in docs]}")
        
        # Filtrar por confianza mínima
        filtered_docs = [doc for doc in docs if doc['score'] >= min_confidence]
        
        # Limitar número de fuentes
        limited_docs = filtered_docs[:max_sources]
        
        if not limited_docs:
            limited_docs = docs[:1]  # Al menos mostrar el mejor resultado
        
        # Paso 2: Generar respuesta
        answer = self.generator.generate_answer(question, limited_docs)
        
        # Paso 3: Formatear respuesta con fuentes
        return {
            "answer": answer,
            "sources": [{"title": doc['title'], "url": doc['url']} for doc in limited_docs]
        }