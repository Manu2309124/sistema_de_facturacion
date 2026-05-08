"""
Inicialización y gestión de base de datos
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import StaticPool

db = SQLAlchemy()


def init_db(app):
    """
    Inicializa la base de datos con la aplicación Flask
    
    Args:
        app: Instancia de aplicación Flask
    """
    db.init_app(app)
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✓ Base de datos inicializada correctamente")


def create_tables(app):
    """
    Crea todas las tablas de la base de datos
    
    Args:
        app: Instancia de aplicación Flask
    """
    with app.app_context():
        db.create_all()


def drop_all_tables(app):
    """
    ADVERTENCIA: Elimina todas las tablas de la base de datos
    
    Args:
        app: Instancia de aplicación Flask
    """
    with app.app_context():
        db.drop_all()
        print("⚠ Todas las tablas han sido eliminadas")


def reset_database(app):
    """
    Reinicia la base de datos: elimina y crea todas las tablas
    
    Args:
        app: Instancia de aplicación Flask
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✓ Base de datos reiniciada correctamente")
