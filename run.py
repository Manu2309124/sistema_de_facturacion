import os
from app import create_app
from app.database import db

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    """Contexto shell para CLI de Flask"""
    return {
        'db': db,
        'app': app
    }

@app.before_request
def before_request():
    """Asegurar que las tablas existen antes de cada request"""
    if not os.path.exists(os.path.join(app.instance_path, 'billing_system.db')):
        db.create_all()

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Limpiar sesión de BD al terminar el contexto"""
    db.session.remove()

@app.errorhandler(404)
def not_found_error(error):
    """Manejar error 404"""
    from flask import jsonify
    return jsonify({'error': 'Endpoint no encontrado', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejar error 500"""
    from flask import jsonify
    db.session.rollback()
    return jsonify({'error': 'Error interno del servidor', 'status': 500}), 500

if __name__ == '__main__':
    # Crear directorio de instancia si no existe
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Crear base de datos
    with app.app_context():
        db.create_all()
    
    # Ejecutar servidor
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
