# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр db здесь
db = SQLAlchemy()

from .project import Project
from .task import Task, TaskPriority, TaskStatus