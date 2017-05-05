from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, func, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///navaras_qa.db'

Base = SQLAlchemy(app)
migrate = Migrate(app, Base)

manager = Manager(app)
manager.add_command('Base', MigrateCommand)

class Genre(Base.Model):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Language(Base.Model):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Movies(Base.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    directedBy = Column(String, nullable=True)
    producedBy = Column(String, nullable=True)
    starringBy = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    musicBy = Column(String, nullable=True)
    language_id = Column(Integer, ForeignKey(Language.id))
    youtube_id = Column(String, nullable=True)
    yt_thumbnail = Column(String, nullable=True)
    yt_videolink = Column(String, nullable=True)
    ref = Column(String, nullable=True)
    language = relationship('Language', foreign_keys=[language_id])


engine = create_engine('sqlite:///navaras_qa.db')
Base.metadata.create_all(engine)

if __name__ == '__main__':
    manager.run()