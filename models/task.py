# models/task.py
import enum
from datetime import datetime
from . import db

class TaskStatus(enum.Enum):
    NEW = "Новая"
    IN_PROGRESS = "В работе"
    REVIEW = "На проверке"
    COMPLETED = "Завершена"

    def __str__(self):
        return self.value

class TaskPriority(enum.Enum):
    LOW = "Низкий"
    MEDIUM = "Средний"
    HIGH = "Высокий"

    def __str__(self):
        return self.value

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.NEW)
    priority = db.Column(db.Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    assignee = db.Column(db.String(100), nullable=False, default='Не назначен')
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.name}>'