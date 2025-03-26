from flask import request, jsonify
from .dependencies import get_intent_classifier, get_rag_system
from .schemas import validate_chat_request
import logging

logger = logging.getLogger(__name__)

def configure_routes(app):
    @app.route('/api/v1/chat', methods=['POST'])
    def chat():
        """
        Endpoint principal del chatbot
        Integra clasificación de intenciones y sistema RAG
        """
        # Validar entrada
        data, errors = validate_chat_request(request)
        if errors:
            return jsonify({
                "status": "error",
                "errors": errors
            }), 400
        
        message = data['message']
        use_rag = data.get('use_rag', True)
        
        try:
            # Clasificar la intención
            intent_classifier = get_intent_classifier()
            intent_result = intent_classifier.predict(message)
            
            # Si la confianza es baja o se solicita explícitamente, usar RAG
            rag_system = get_rag_system()
            if use_rag:
            # if use_rag or intent_result['confidence'] < 0.4:
                rag_response = rag_system.query(
                                                message,
                                                max_sources=1,  # Limitar a 1 fuente principal
                                                min_confidence=0.65
                                            )
                return jsonify({
                    "status": "success",
                    "response": rag_response['answer'],
                    "sources": rag_response['sources'],
                    # "intent": intent_result['intent'],
                    # "confidence": intent_result['confidence'],
                    "response_type": "rag"
                })
            
            # Respuesta basada en intención
            return jsonify({
                "status": "success",
                "response": intent_result.get('response', ''),
                "intent": intent_result['intent'],
                "confidence": intent_result['confidence'],
                "response_type": "intent"
            })
            
        except Exception as e:
            logger.error(f"Error en el endpoint /chat: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Error procesando la solicitud"
            }), 500

    @app.route('/api/v1/rag/query', methods=['POST'])
    def rag_query():
        """
        Endpoint específico para consultas al sistema RAG
        """
        data, errors = validate_chat_request(request)
        if errors:
            return jsonify({"status": "error", "errors": errors}), 400
        
        try:
            rag_system = get_rag_system()
            response = rag_system.query(data['message'], max_sources=1, min_confidence=0.65)
            return jsonify({
                "status": "success",
                "response": response['answer'],
                "sources": response['sources']
            })
        except Exception as e:
            logger.error(f"Error en RAG query: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Error en el sistema RAG"
            }), 500

    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        """Endpoint de verificación de salud"""
        return jsonify({
            "status": "healthy",
            "version": "1.0.0",
            "services": {
                "intent_classifier": "operational",
                "rag_system": "operational"
            }
        })