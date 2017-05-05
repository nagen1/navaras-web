from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy, Pagination
from databasenew import Movies
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///navaras_qa.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


movies = dbsession.query(Movies).all()

#list = Movies.query.paginate(page=2, per_page=20)
pager = Movies.query.filter(Movies.youtube_id != None).paginate(page=2, per_page=20)
print(pager)

#for item in list.items:
 #   print(item.title)

#genre = Movies.query.filter(Movies.genre.contains('drama'))

#for gen in genre:
#    print(gen.title, ":", gen.genre)

