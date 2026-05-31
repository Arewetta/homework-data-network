# config.py
import os

class Config:
    SECRET_KEY = 'your-secret-key-change-this'
    
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASEDIR, "instance", "project_manager.db")}'

    WTF_CSRF_ENABLED = True

    BABEL_DEFAULT_LOCALE = 'ru'