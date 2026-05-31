# routes/__init__.py
from flask import Blueprint, redirect, url_for
from .project_routes import project_bp
from .task_routes import task_bp

# Создаем главный blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Перенаправляем с корня на список проектов"""
    return redirect(url_for('project.index'))

def register_blueprints(app):
    app.register_blueprint(main_bp)  # Регистрируем главный маршрут
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)