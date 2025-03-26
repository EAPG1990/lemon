import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

def setup_logging(app):
    """Configura el sistema de logging para la aplicación"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler para archivo
    file_handler = RotatingFileHandler(
        logs_dir / 'lemon_api.log',
        maxBytes=1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    
    # Aplicar handlers
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)
    
    # Eliminar handler por defecto de Flask
    app.logger.removeHandler(app.logger.handlers[0])