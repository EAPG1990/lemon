from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline

class IntentPredictor:
    def __init__(self, model_path=None):
        self.model_path = model_path or Path(__file__).parent / "data" / "models" / "intent_model.pkl"
        self.model = self.load_model()
    
    def load_model(self):
        """Carga el modelo entrenado"""
        try:
            return joblib.load(self.model_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Modelo no encontrado en {self.model_path}. "
                "Por favor entrena el modelo primero ejecutando trainer.py"
            )
    
    def predict(self, text):
        """Predice la intención de un texto"""
        if not isinstance(text, str) or not text.strip():
            return {"intent": "unknown", "confidence": 0.0}
            
        intent = self.model.predict([text])[0]
        probas = self.model.decision_function([text])[0]
        confidence = max(probas)  # Usamos el score de decisión como confianza
        
        return {
            "intent": intent,
            "confidence": float(confidence),
            "probabilities": dict(zip(self.model.classes_, probas))
        }

if __name__ == "__main__":
    # Ejemplo de uso
    predictor = IntentPredictor()
    test_phrases = [
        "¿Cómo retiro mis bitcoins?",
        "No reconozco esta transacción",
        "Quiero información sobre Lemon Earn",
        "Perdí mi tarjeta, ¿qué hago?"
    ]
    
    for phrase in test_phrases:
        result = predictor.predict(phrase)
        print(f"\nFrase: '{phrase}'")
        print(f"Intención predicha: {result['intent']} (confianza: {result['confidence']:.2f})")