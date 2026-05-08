import os
from datetime import timedelta

class Config:
    """Configuración base para todas los entornos"""
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # JSON
    JSON_SORT_KEYS = False
    

class DevelopmentConfig(Config):
    """Configuración de Desarrollo con SQLite"""
    DEBUG = True
    TESTING = False
    
    # SQLite Database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_NAME = 'billing_system.db'
    DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'instance', DB_NAME)
    
    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_ECHO = True  # Log todas las queries SQL
    
    # Opciones de SQLite
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'timeout': 15,  # timeout en segundos
            'check_same_thread': False  # Permite múltiples threads
        },
        'pool_pre_ping': True,  # Verifica conexiones antes de usarlas
        'pool_recycle': 3600,  # Recicla conexiones cada hora
    }
    
    # Development settings
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    

class TestingConfig(Config):
    """Configuración de Testing - BD en memoria"""
    DEBUG = True
    TESTING = True
    
    # SQLite In-Memory Database para tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    
    # Opciones de SQLite
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'timeout': 15,
            'check_same_thread': False
        }
    }
    

class ProductionConfig(Config):
    """Configuración de Producción"""
    DEBUG = False
    TESTING = False
    
    # SQLite o PostgreSQL en producción
    DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite')
    
    if DB_ENGINE == 'sqlite':
        # SQLite para producción
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        DB_NAME = os.environ.get('DB_NAME', 'billing_system_prod.db')
        DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', DB_NAME)
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    else:
        # PostgreSQL alternativa
        DB_USER = os.environ.get('DB_USER')
        DB_PASS = os.environ.get('DB_PASSWORD')
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_PORT = os.environ.get('DB_PORT', '5432')
        DB_NAME = os.environ.get('DB_NAME', 'billing_system')
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # SQLAlchemy Configuration
    SQLALCHEMY_ECHO = False
    
    # Opciones de SQLite
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'timeout': 30,
            'check_same_thread': False
        },
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 3600,
    }
    

class FactoryConfig(Config):
    """Configuración para Factory Pattern"""
    pass


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
