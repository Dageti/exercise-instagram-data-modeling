import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
import enum

Base = declarative_base()

class MediaType(enum.Enum):
    image = "image"
    video = "video"

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    firstname = Column(String(20), unique=False, nullable=False)
    lastname = Column(String(20), unique=False, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    #relationships
    post = relationship('Post', backref='user')
    comments = relationship('Comment', backref='author')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum(MediaType), nullable=False)
    url = Column(String(200), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'),nullable=False)

    # Relationships
    post = relationship('Post', backref='media')


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(300), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
  

class Follower(Base):
    __tablename__ = 'follower'

    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    
    # relationships
    user_from = relationship('user', foreign_keys=[user_from_id], backref='following')
    user_to = relationship('user', foreign_keys=[user_to_id], backref='followers')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
