from pathlib import Path
from email_processor import EmailProcessor
from config import INPUT_EMAILS_DIR, OUTPUT_DIR

def main():
    input_file = INPUT_EMAILS_DIR / "emails.csv"
    output_file = OUTPUT_DIR / "processed_emails.csv"
    
    processor = EmailProcessor()
    processor.process_file(input_file, output_file)
    
    # Mostrar resultados para depuración
    with open(output_file, 'r') as f:
        print("Resultados procesados:")
        print(f.read())

if __name__ == "__main__":
    main()