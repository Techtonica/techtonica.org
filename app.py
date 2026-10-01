import os
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ... (restante do código de inicialização do app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    
    # Check for development SSL certificate environment variable
    # If FLASK_RUN_CERT is set, Flask will use pyopenssl to generate an ad-hoc cert
    if os.environ.get('FLASK_ENV') == 'development' and os.environ.get('FLASK_RUN_CERT'):
        app.run(ssl_context='adhoc')
    else:
        app.run()
