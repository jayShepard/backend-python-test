import json

from alayatodo import app
from alayatodo.forms import LoginForm, TodoForm
from alayatodo.models import User, Todo

from flask_paginate import Pagination, get_page_parameter, get_page_args
from flask import (g, redirect, render_template, request, session, flash)


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    if session.get('logged_in'):
        return redirect('/todo')

    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def login_POST():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Invalid username')
            return redirect('/login')

        if not user.verify_password(password):
            flash('Invalid password')
            return redirect('login')

        session['user'] = user.to_dict()
        session['logged_in'] = True
        return redirect('/todo')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/login')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    if not session.get('logged_in'):
        redirect('/login')

    form = TodoForm()

    todo = Todo.query.filter_by(
        id=id, user_id=session.get('user')['id']).first()
    if not todo:
        return render_template('404.html'), 404

    return render_template('todo.html', todo=todo, form=form)


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return json.dumps(
            {'error': 401, 'message': "Must be logged in to view"}), 401

    todo = Todo.query.filter_by(
        id=id, user_id=session.get('user')['id']).first()
    if not todo:
        return json.dumps({'error': 404, 'message': 'task not found'}), 404

    return json.dumps(todo.to_dict())

@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    form = TodoForm()
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    todos =  Todo.query.filter_by(
        user_id=session['user']['id']).offset(offset).limit(per_page)

    pagination = Pagination(page=page, total=Todo.query.count(),
                            search=search, record_name='todos',
                            format_total=True, format_number=True,
                            per_page=per_page)

    return render_template(
        'todos.html', todos=todos, form=form, pagination=pagination)

@app.route('/todo/<id>', methods=['POST'])
def todos_PUT(id):
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user']['id']
    is_completed = bool(request.form.get('completed', False))

    todo = Todo.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return render_template('404.html'), 404

    todo.is_completed = is_completed
    g.db.add(todo)
    flash("Task completed!") if is_completed else flash("Task Uncompleted!")
    g.db.commit()
    return redirect('/todo')


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    user_id = session['user']['id']
    description = request.form.get('description', '')
    todo = Todo(
        user_id=user_id, description=description, is_completed=False)
    g.db.add(todo)
    g.db.commit()
    flash("You have new thing to do!")
    return redirect('/todo')

@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if not todo:
        return render_template('404.html'), 404

    g.db.delete(todo)
    g.db.commit()
    flash("You removed a task!")
    return redirect('/todo')
