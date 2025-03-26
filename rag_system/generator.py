from sentence_transformers import SentenceTransformer
import numpy as np

class AnswerGenerator:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    def generate_answer(self, question: str, contexts) -> str:
        """Genera respuestas mejor formateadas priorizando el mejor contexto
        
        Args:
            question: Pregunta del usuario
            contexts: Lista de contextos recuperados (debe contener 'content', 'score', 'url')
        
        Returns:
            Respuesta formateada con información relevante
        """
        if not contexts:
            return ("No encontré información específica sobre este tema en el centro de ayuda. "
                    "Por favor contacta a soporte@lemon.me para asistencia personalizada.")
        
        # Seleccionar el contexto con mayor puntaje
        best_context = max(contexts, key=lambda x: x['score'])
        
        # Limpiar y preparar el contenido
        cleaned_content = self._clean_content(best_context['content'])
        
        # Extraer los puntos más relevantes (primeros 3 párrafos o 500 caracteres)
        main_info = "\n".join(cleaned_content.split("\n")[:3])[:500]
        
        # # Construir respuesta estructurada
        # return (
        #     f"**Pregunta:** {question}\n\n"
        #     f"**Respuesta oficial de Lemon:**\n{main_info}\n\n"
        #     f"**Fuente completa:** {best_context.get('url', '')}\n"
        #     f"**Relevancia:** {best_context['score']:.0%}"
        # )
        return (
            f"{main_info}\n\n"
            f"**Relevancia:** {best_context['score']:.0%}"
        )
    
    def _clean_content(self, content: str) -> str:
        """Limpia el contenido del contexto removiendo metadatos innecesarios"""
        lines_to_skip = {
            'Escrito por', 'Actualizado', 'Artículos relacionados', 
            'Leer más en', 'También te puede interesar'
        }
        
        return "\n".join(
            line.strip() for line in content.split('\n')
            if (line.strip() and 
                not any(skip in line for skip in lines_to_skip) and
                not line.startswith('_'))
        )