from flask import Flask, jsonify
from .endpoints import configure_routes
from .utils.logging import setup_logging
import os

def create_app():
    # Crear aplicación Flask
    app = Flask(__name__)
    
    # Configuración básica
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSON_AS_ASCII'] = False
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar blueprints/routes
    configure_routes(app)
    
    # Manejo de errores global
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "status": "error",
            "message": "Endpoint no encontrado"
        }), 404
    
    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f"Error en el servidor: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Error interno del servidor"
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)