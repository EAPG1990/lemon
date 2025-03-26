from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class EmailSummarizer:
    def __init__(self):
        self.stop_words = set(stopwords.words('spanish') + stopwords.words('english'))
        
    def summarize(self, text: str, max_sentences: int = 3) -> str:
        """Simple extractive summarization"""
        sentences = sent_tokenize(text)
        if len(sentences) <= max_sentences:
            return ' '.join(sentences)
            
        word_freq = defaultdict(int)
        for word in text.lower().split():
            if word not in self.stop_words:
                word_freq[word] += 1
                
        ranked_sentences = sorted(
            sentences,
            key=lambda s: sum(word_freq[word] for word in s.lower().split()),
            reverse=True
        )
        
        return ' '.join(ranked_sentences[:max_sentences])