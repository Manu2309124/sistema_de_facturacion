import os
from app import create_app
from app.database import db

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

@app.before_request
def before_request():
    """Create tables if they don't exist"""
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
