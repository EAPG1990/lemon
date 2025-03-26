import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Data paths
INPUT_EMAILS_DIR = BASE_DIR / "data" / "input_emails"
OUTPUT_DIR = BASE_DIR / "data" / "output"

# Ensure directories exist
os.makedirs(INPUT_EMAILS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Email processing parameters
EMAIL_CATEGORIES  = {
    "crypto": ["cripto", "bitcoin", "ethereum", "blockchain"],
    "banking": ["cuenta", "transferencia", "depósito", "retiro", "cvu"],
    "tarjeta": ["tarjeta", "visa", "mastercard", "pago", "compra"],
    "Otro":["otro"]
}