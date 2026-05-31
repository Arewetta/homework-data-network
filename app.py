# app.py
from flask import Flask
from config import Config
from models import db
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализация БД
    db.init_app(app)
    
    # Регистрация маршрутов
    register_blueprints(app)
    
    # Создание таблиц только если их нет
    with app.app_context():
        db.create_all()
        print("База данных проверена/создана успешно!")
        print("Сервер запущен на http://127.0.0.1:5000/")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)