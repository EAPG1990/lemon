import pandas as pd
import random
from pathlib import Path

INTENTS = [
    "Retiros Crypto",
    "Desconocimiento de Transacciones",
    "Retiros Fiat",
    "Denuncia de Tarjeta Perdida",
    "Lemon Earn"
]

EXAMPLES = {
    "Retiros Crypto": [
        "¿Cómo puedo retirar criptomonedas?",
        "Quiero sacar mis bitcoins de la plataforma",
        "¿Cuál es el límite para retiros de ETH?",
        "Tiempo estimado para retiro de cripto",
        "¿Hay comisión por retirar USDT?"
    ],
    "Desconocimiento de Transacciones": [
        "No reconozco una transacción en mi cuenta",
        "Aparece un movimiento que no hice",
        "¿Cómo reporto una operación fraudulenta?",
        "Recibí un débito no autorizado",
        "Alguien más accedió a mi cuenta"
    ],
    "Retiros Fiat": [
        "¿Cómo retiro dinero a mi banco?",
        "Tiempo de transferencia a cuenta bancaria",
        "Límite diario para retiros en pesos",
        "No llega mi transferencia a mi banco",
        "¿Puedo retirar dólares a mi cuenta?"
    ],
    "Denuncia de Tarjeta Perdida": [
        "Perdí mi tarjeta Lemon",
        "¿Cómo bloqueo mi tarjeta extraviada?",
        "Robaron mi tarjeta, ¿qué hago?",
        "Quiero reportar tarjeta perdida",
        "Procedimiento para tarjeta extraviada"
    ],
    "Lemon Earn": [
        "¿Cómo funciona Lemon Earn?",
        "Rendimientos actuales de Earn",
        "¿Puedo retirar mis fondos de Earn cuando quiera?",
        "Riesgos de invertir en Earn",
        "¿Qué criptomonedas están disponibles en Earn?"
    ]
}

def generate_dataset(num_samples=200):
    """Genera un dataset balanceado de ejemplos para cada intención"""
    samples_per_intent = num_samples // len(INTENTS)
    data = []
    
    for intent in INTENTS:
        base_examples = EXAMPLES[intent]
        # Generar variaciones de los ejemplos base
        for _ in range(samples_per_intent):
            example = random.choice(base_examples)
            # Añadir alguna variación aleatoria
            variations = [
                f"{random.choice(['', 'Hola', 'Buenos días', 'Hola equipo'])} {example} {random.choice(['', 'Gracias', 'Por favor ayuda', 'Es urgente'])}",
                f"{example.lower()}",
                f"{example.upper()}",
                f"{example}?",
                f"Quisiera saber {example[0].lower() + example[1:]}"
            ]
            selected = random.choice(variations)
            data.append({"text": selected, "intent": intent})
    
    return pd.DataFrame(data)

def save_dataset(df, path):
    """Guarda el dataset generado"""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    dataset = generate_dataset()
    save_path = Path(__file__).parent / "data" / "intents_dataset.csv"
    save_dataset(dataset, save_path)
    print(f"Dataset generado con {len(dataset)} ejemplos en {save_path}")