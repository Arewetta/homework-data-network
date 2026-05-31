# models/project.py
from . import db
from .task import TaskStatus

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    def get_progress(self):
        """Возвращает процент выполненных задач"""
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return 0
        completed_tasks = sum(1 for task in self.tasks if task.status == TaskStatus.COMPLETED)
        return int((completed_tasks / total_tasks) * 100)
    
    def get_task_count(self):
        return len(self.tasks)

    def __repr__(self):
        return f'<Project {self.name}>'