import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import nltk
from nltk.corpus import stopwords

# Descargar stopwords en español
nltk.download('stopwords')

class IntentTrainer:
    def __init__(self):
        # Obtener stopwords en español
        spanish_stopwords = stopwords.words('spanish')
        
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                lowercase=True,
                stop_words=spanish_stopwords,  # Usar lista de stopwords
                ngram_range=(1, 2),
                max_features=10000
            )),
            ('clf', LinearSVC(
                C=0.8,
                class_weight='balanced',
                max_iter=10000,
                random_state=42
            ))
        ])
    
    def train(self, dataset_path, model_save_path):
        """Entrena el modelo y lo guarda"""
        df = pd.read_csv(dataset_path)
        
        # Verificar datos
        print("\nMuestra del dataset:")
        print(df.sample(5))
        
        X_train, X_test, y_train, y_test = train_test_split(
            df['text'], df['intent'], test_size=0.2, random_state=42
        )
        
        print("\nEntrenando modelo...")
        self.model.fit(X_train, y_train)
        
        # Evaluación
        print("\nEvaluación en conjunto de prueba:")
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        
        # Guardar modelo
        model_save_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, model_save_path)
        print(f"\nModelo guardado en {model_save_path}")

if __name__ == "__main__":
    # Ejecutar directamente (no como módulo)
    data_path = Path("intent_classifier/data/intents_dataset.csv")
    model_path = Path("intent_classifier/data/models/intent_model.pkl")
    
    print("Iniciando entrenamiento...")
    trainer = IntentTrainer()
    trainer.train(data_path, model_path)