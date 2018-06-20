__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from examples.connector import Base, engine, session
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

tags = Table('tag_image', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('image_id', Integer, ForeignKey('images.id'))
)

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    tags = relationship('Tag', secondary=tags, backref = backref('images', lazy='dynamic'))
    comments = relationship('Comment', backref='image', lazy='dynamic')

    def __repr__(self):
        str_created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<Image (uuid={}, likes={}, created_at={})>".format(self.uuid, self.likes, str_created_at)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return "<Tag (name='%s')>" % (self.name)

class Comment(Base):
    __tablename__ = 'comments'

    id  = Column(Integer, primary_key=True)
    text = Column(String(2000))
    image_id = Column(Integer, ForeignKey('images.id'))

    def __repr__(self):
        return "<Comment (text='%s')>" % (self.text)

# Base.metadata.create_all(engine)