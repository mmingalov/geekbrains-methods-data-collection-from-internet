#к уроку 2

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    Integer
)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#промежуточная таблица (ассоциатив) для связки тэгов с постами в связи Многое ко Многому
assoc_post_tag = Table(
    'post_tag',
    Base.metadata,
    Column('blogpost', Integer, ForeignKey('blogpost.id')),
    Column('tag', Integer, ForeignKey('tag.id'))
)
#todo класс записи в блоге
class BlogPost(Base):
    __tablename__ = 'blogpost'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    url = Column(String, unique=True)
    writer_id = Column(Integer, ForeignKey('writer.id'))
    writer = relationship('Writer', backref='blogposts')
    tages = relationship('Tag', secondary=assoc_post_tag, backref='blogposts')

    def __init__(self, title: str, url: str, writer, tags=tuple()):
        self.title = title
        self.url = url
        self.writer = writer
        if tags:
            self.tags.extend(tags)

#todo класс для объекта тэга
class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    def __init__(self, name: str):
        self.name = name

#todo класс для автора поста
class Writer(Base):
    __tablename__ = 'writer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    url = Column(String, unique=True)
    name = Column(String)

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
