from intent_classifier import IntentPredictor
from rag_system import RAGSystem
import threading

# Singleton instances with thread lock
_intent_classifier = None
_rag_system = None
_lock = threading.Lock()

def get_intent_classifier():
    global _intent_classifier
    if _intent_classifier is None:
        with _lock:
            if _intent_classifier is None:
                _intent_classifier = IntentPredictor()
    return _intent_classifier

def get_rag_system():
    global _rag_system
    if _rag_system is None:
        with _lock:
            if _rag_system is None:
                _rag_system = RAGSystem()
    return _rag_system