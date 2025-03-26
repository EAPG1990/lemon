from flask import request
from typing import Tuple, Dict, Any

def validate_chat_request(req) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Valida la estructura de la solicitud de chat
    Returns:
        tuple: (data, errors)
    """
    data = req.get_json(silent=True) or {}
    errors = {}
    
    if not data.get('message'):
        errors['message'] = "El mensaje es requerido"
    
    if not isinstance(data.get('message', ''), str):
        errors['message'] = "El mensaje debe ser texto"
    
    if len(data.get('message', '')) > 1000:
        errors['message'] = "El mensaje es demasiado largo"
    
    return data, errors