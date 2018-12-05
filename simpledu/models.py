from datetime import datetime

from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# 注意这里不再传入 app 了
from .exts import db


class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    __password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    job = db.Column(db.String(64))
    publish_courses = db.relationship('Course')

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, pwd):
        self.__password = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self.__password, pwd)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF


class Course(BaseModel):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author = db.relationship('User', uselist=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(256))
    chapters = db.relationship("Chapter")

    def __repr__(self):
        return self.name

    @property
    def url(self):
        return url_for('course.detail', id=self.id)


class Chapter(BaseModel):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(256))
    video_duration = db.Column(db.String(24))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id", ondelete="CASCADE"))
    course = db.relationship("Course")

    def __repr__(self):
        return self.name

    @property
    def url(self):
        return url_for('course.chapter', course_id=self.course.id, chapter_id=self.id)
