import pandas as pd
from pathlib import Path
from .classifier import EmailClassifier
from .cvu_extractor import CVUExtractor
from .summarizer import EmailSummarizer
from config import INPUT_EMAILS_DIR, OUTPUT_DIR  # Importar directamente desde config

class EmailProcessor:
    def __init__(self):
        self.classifier = EmailClassifier()
        self.cvu_extractor = CVUExtractor()
        self.summarizer = EmailSummarizer()
        
    def process_file(self, input_path: Path, output_path: Path):
        """Process email file and save results."""
        # Read input file
        if input_path.suffix == '.csv':
            df = pd.read_csv(input_path)
        elif input_path.suffix == '.json':
            df = pd.read_json(input_path, orient='records')
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
            
        # Process each email
        results = []
        for _, row in df.iterrows():
            result = self.process_email(row)
            results.append(result)
            
        # Save results
        output_df = pd.DataFrame(results)
        output_df.to_csv(output_path, index=False)
        
    # email_processor/processor.py
    def process_email(self, email_data: pd.Series) -> dict:
        """Process a single email."""
        raw_body = str(email_data['Cuerpo del mensaje'])
        category = self.classifier.classify(
            str(email_data['Asunto']), 
            raw_body
        )
        
        summary = self.summarizer.summarize(raw_body)
        cvu = ""
        
        # Extracción condicional más robusta
        if 'banking' in category.lower():
            cvu = self.cvu_extractor.extract(raw_body)
            print(f"Debug - CVU encontrado: {cvu}")  # Línea de depuración
            
        return {
            "ID del cliente": str(email_data['ID del cliente']),
            "Asunto": str(email_data['Asunto']),
            "Categoría": category,
            "Resumen": summary,
            "CVU": cvu
        }