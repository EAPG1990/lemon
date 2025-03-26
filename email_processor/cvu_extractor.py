import re

class CVUExtractor:
    def __init__(self):
        # Patrón mejorado para CVU (22 dígitos consecutivos)
        # Acepta espacios, guiones o puntos como separadores
        self.pattern = re.compile(
            r'(?:CVU|Clave Virtual Uniforme)[:\-\s]*([\d\s\-\.]{22,})|'
            r'\b(\d[\d\s\-\.]{20,}\d)\b'
        )
        
    def extract(self, text: str) -> str:
        """Extrae CVU del texto y lo normaliza (solo dígitos)"""
        matches = self.pattern.search(text)
        if not matches:
            return ""
            
        # Tomar el primer grupo que coincida
        cvu = matches.group(1) if matches.group(1) else matches.group(2)
        
        # Normalizar: quitar todos los caracteres no numéricos
        cvu_clean = re.sub(r'[^\d]', '', cvu)
        
        # Validar que tenga exactamente 22 dígitos
        return cvu_clean if len(cvu_clean) == 22 else ""