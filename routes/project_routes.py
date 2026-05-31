# routes/project_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Project, Task, TaskStatus  # Добавлен импорт Task и TaskStatus

project_bp = Blueprint('project', __name__, url_prefix='/project')

@project_bp.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@project_bp.route('/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('project_detail.html', project=project, tasks=tasks, TaskStatus=TaskStatus)

@project_bp.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        if not name or not start_date_str:
            flash('Название и дата начала обязательны', 'danger')
            return render_template('project_form.html', project=None)
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = None
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if end_date < start_date:
                flash('Дата окончания не может быть раньше даты начала', 'danger')
                return render_template('project_form.html', project=None)
        
        project = Project(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(project)
        db.session.commit()
        flash('Проект успешно создан', 'success')
        return redirect(url_for('project.index'))
    
    return render_template('project_form.html', project=None)

@project_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        if not name or not start_date_str:
            flash('Название и дата начала обязательны', 'danger')
            return render_template('project_form.html', project=project)
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = None
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if end_date < start_date:
                flash('Дата окончания не может быть раньше даты начала', 'danger')
                return render_template('project_form.html', project=project)
        
        project.name = name
        project.description = description
        project.start_date = start_date
        project.end_date = end_date
        
        db.session.commit()
        flash('Проект успешно обновлён', 'success')
        return redirect(url_for('project.index'))
    
    return render_template('project_form.html', project=project)

@project_bp.route('/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Проект и все его задачи удалены', 'success')
    return redirect(url_for('project.index'))