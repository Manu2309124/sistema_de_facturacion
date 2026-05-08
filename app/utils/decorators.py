"""Custom decorators for the application"""
from functools import wraps
from flask import jsonify

def handle_exceptions(f):
    """Decorator to handle exceptions in route handlers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return decorated_function

def validate_json(f):
    """Decorator to validate JSON request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request
        if not request.is_json:
            return jsonify({'error': 'Invalid JSON'}), 400
        return f(*args, **kwargs)
    return decorated_function
