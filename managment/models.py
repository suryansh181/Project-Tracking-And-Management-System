from datetime import datetime
from managment import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

works = db.Table('works',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    Projects = db.relationship('Project', backref='creator', lazy=True)
    work=db.relationship('Project',secondary= works,backref=db.backref('onproject',lazy=True))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    content = db.Column(db.Text, nullable=False)
    project_file = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Tasks= db.relationship('Task', backref='parent',passive_deletes=True, lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.deadline}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.Text, nullable=False)
    task_file = db.Column(db.String(20))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id',ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.deadline}')"
