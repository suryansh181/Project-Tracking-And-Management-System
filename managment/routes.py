import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request,session
from managment import app, db, bcrypt, mail
from managment.form import RegistrationForm, LoginForm, UpdateAccountForm, ProjectForm,TaskForm,TeamForm
from managment.models import User, Project,Task,works
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message, Mail




@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('project'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('project'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pic', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        # flash('Your profile have been updated!','success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    image_file = url_for(
        'static', filename='profile_pic/'+current_user.image_file)
    return render_template('profile.html', image_file=image_file, form=form)

# @app.route("/notification")
# @login_required
# def notification():
#     return render_template('notification.html')


def save_file(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    project_file_fn = random_hex + f_ext
    project_file_path = os.path.join(
        app.root_path, 'static/project_file', project_file_fn)
    # file=open(project_file)
    form_file.save(project_file_path)
    return project_file_fn


@app.route("/project", methods=['GET', 'POST'])
@login_required
def project():
    projects = Project.query.filter(Project.user_id == current_user.id)
    form = ProjectForm()
    if form.validate_on_submit():
        if form.project_file.data:
            project_file = save_file(form.project_file.data)
        p = Project(title=form.title.data, content=form.content.data,
                    project_file=project_file, deadline=form.deadline.data, creator=current_user)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('project'))
    return render_template('project.html', form=form, projects=projects)

@app.route("/project/<int:project_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.creator != current_user:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    # flash('Your post has been deleted!', 'success')
    return redirect(url_for('project'))


# @app.route("/task")
# @login_required
# def task():
#     return render_template('task.html')

def save_task(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    task_file_fn = random_hex + f_ext
    task_file_path = os.path.join(
        app.root_path, 'static/task_file', task_file_fn)
    form_file.save(task_file_path)
    return task_file_fn

@app.route("/task")
@app.route("/task/<int:project_id>",methods=['GET', 'POST'])
@login_required
def task( project_id = None):
    session['project_id'] = project_id
    tasks = Task.query.filter(Task.project_id == project_id)
    form = TaskForm()
    if form.validate_on_submit():
        if form.task_file.data:
            task_file = save_task(form.task_file.data)
        t = Task(title=form.title.data, content=form.content.data,task_file=task_file, deadline=form.deadline.data,project_id=project_id)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('task', project_id=project_id))
    return render_template('task.html', form=form, tasks=tasks, project_id=project_id)

@app.route("/task/<int:task_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    project_id=task.project_id
    # if task.creator != current_user:
    #     abort(403)
    db.session.delete(task)
    db.session.commit()
    # flash('Your post has been deleted!', 'success')
    return redirect(url_for('task', project_id=project_id))

# @app.route("/team")
# @app.route("/team/<int:project_id>",methods=['GET', 'POST'])
# @login_required
# def team(project_id = None):
#     project = Project.query.get_or_404(project_id)
#     team_mem = User.query.join(User,Project).filter(Project.project_id==project_id)
#     # Artist._albums.any(id=album1.id)).all()
#     form = TeamForm()
#     if form.validate_on_submit():
#         email_id = form.email.data
#         u=User.query.get(user.email==email_id)
#         project.onproject.append(u.id)
#         db.session.commit()
#         return redirect(url_for('team', project_id=project_id))
#     return render_template('team.html', form=form, team_mem=team_mem, project_id=project_id)

@app.route("/team")
@app.route("/team/<int:project_id>",methods=['GET', 'POST'])
@login_required
def team(project_id = None):
    session['project_id'] = project_id
    project = Project.query.filter(Project.id == project_id).first()
    if project_id:
        users = db.session.query(User.username, User.email).filter(works.c.user_id == User.id).filter(works.c.project_id == project.id).all()
    else:
        users= None
    form = TeamForm()
    if form.validate_on_submit():
        email_id = form.email.data
        user = User.query.filter(User.email == email_id).first()
        # w = works(user_id=user.id, project_id=project_id)
        stmnt = works.insert().values(user_id=user.id, project_id=project_id)
        db.session.execute(stmnt) 
        db.session.commit()
        return redirect(url_for('team',project_id=project_id))
    return render_template('team.html',form=form,users=users, project_id=project_id)

@app.route("/message", methods=['GET', 'POST'])
@login_required
def message():
    if request.method == "POST":
        email = request.form['email']
        subject = request.form['subject']
        msg = request.form['message']
        message = Message(subject, sender="project.mngmt4you@gmail.com",
                          recipients=['project.mngmt4you@gmail.com'])
        message.body = msg
        mail.send(message)
        return redirect(url_for('message'))
    success = "Message sent"
    return render_template('message.html', success=success)


@app.route("/invite", methods=['GET', 'POST'])
@login_required
def invite():
    if request.method == "POST":
        email = request.form['email']
        subject = 'Invitation To Project Manager'
        message = Message(subject, sender="project.mngmt4you@gmail.com",
                          recipients=['project.mngmt4you@gmail.com'])
        message.html= render_template('email.html')
        mail.send(message)
        return redirect(url_for('invite'))
    success = "Message sent"
    return render_template('invite.html', success=success)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))
