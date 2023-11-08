from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user' #테이블 이름

    id = db.Column(db.Integer, primary_key=True) # 자동으로 증가하는 User 모델의 기본 키
    username = db.Column(db.String(100), unique=True, nullable=False) # 같은 값 저장 X, 빈 값 X
    password = db.Column(db.String(20), nullable=False) # 빈 값 X

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(1000))
    datetime = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
    user = db.relationship('User', backref=db.backref('post_set'))
    username = db.Column(db.String(100), db.ForeignKey('user.username', ondelete='CASCADE')) # Post에 username을 저장하는 user_id column 생성

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    post = db.relationship('Post', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    datetime = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Text(), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')
    datetime = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
