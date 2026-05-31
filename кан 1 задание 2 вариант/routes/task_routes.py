# routes/task_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Project, Task, TaskStatus, TaskPriority, db  

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/project/<int:project_id>/add', methods=['GET', 'POST'])
def add_task(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status_str = request.form.get('status')
        priority_str = request.form.get('priority')
        assignee = request.form.get('assignee')
        
        if not name or not assignee:
            flash('Название задачи и исполнитель обязательны', 'danger')
            return render_template('task_form.html', task=None, project=project, 
                                 TaskStatus=TaskStatus, TaskPriority=TaskPriority)
        
        status = TaskStatus[status_str] if status_str else TaskStatus.NEW
        priority = TaskPriority[priority_str] if priority_str else TaskPriority.MEDIUM
        
        task = Task(
            name=name,
            description=description,
            status=status,
            priority=priority,
            assignee=assignee,
            project_id=project_id
        )
        db.session.add(task)
        db.session.commit()
        flash('Задача успешно создана', 'success')
        return redirect(url_for('project.view_project', project_id=project_id))
    
    return render_template('task_form.html', task=None, project=project, 
                         TaskStatus=TaskStatus, TaskPriority=TaskPriority)

@task_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    project = task.project
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status_str = request.form.get('status')
        priority_str = request.form.get('priority')
        assignee = request.form.get('assignee')
        
        if not name or not assignee:
            flash('Название задачи и исполнитель обязательны', 'danger')
            return render_template('task_form.html', task=task, project=project, 
                                 TaskStatus=TaskStatus, TaskPriority=TaskPriority)
        
        task.name = name
        task.description = description
        task.status = TaskStatus[status_str]
        task.priority = TaskPriority[priority_str]
        task.assignee = assignee
        
        db.session.commit()
        flash('Задача успешно обновлена', 'success')
        return redirect(url_for('project.view_project', project_id=project.id))
    
    return render_template('task_form.html', task=task, project=project, 
                         TaskStatus=TaskStatus, TaskPriority=TaskPriority)

@task_bp.route('/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    project_id = task.project_id
    
    db.session.delete(task)
    db.session.commit()
    flash('Задача удалена', 'success')
    return redirect(url_for('project.view_project', project_id=project_id))