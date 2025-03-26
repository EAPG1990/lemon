from config import EMAIL_CATEGORIES

class EmailClassifier:
    def __init__(self):
        self.categories = EMAIL_CATEGORIES
        
    def classify(self, subject: str, body: str) -> str:
        """Classify email based on subject and body content."""
        combined_text = f"{subject.lower()} {body.lower()}"
        
        for category, keywords in self.categories.items():
            if any(keyword.lower() in combined_text for keyword in keywords):
                return f"Consultas de {category.capitalize()}"
                
        return "Otro"