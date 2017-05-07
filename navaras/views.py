"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from navaras import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine, and_
from flask_sqlalchemy import SQLAlchemy
from databasenew import Movies, Genre
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///navaras_qa.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/movies/')
@app.route('/movies/<int:page>')
def movies(page=None):

    if page:
        try:
            #movies = dbsession.query(Movies).filter(Movies.youtube_id != None).all()
            movies = Movies.query.filter(Movies.youtube_id != None).paginate(page=page, per_page=20)

        except NoResultFound:
            None
    else:
        try:
            movies = Movies.query.filter(Movies.youtube_id != None).paginate(page=1, per_page=20)

        except NoResultFound:
            None

    return render_template('movies/index.html', movies=movies)


@app.route('/movies/list/<int:year>')
def movielist(year):
    try:
        movies = dbsession.query(Movies).filter(and_(Movies.year == year, Movies.youtube_id == None)).all()
    except NoResultFound:
        None

    return render_template('movies/list.html', list=movies)


@app.route('/movieEdit/<int:movie_id>', methods=['GET','POST'])
def movieEdit(movie_id):
    try:
        movie = dbsession.query(Movies).filter(Movies.id == movie_id).one()
    except NoResultFound:
        None

    if request.method == 'POST':
        movie.title = request.form['title']
        movie.directedBy = request.form['directedBy']
        movie.producedBy = request.form['producedBy']
        movie.starringBy = request.form['starringBy']
        movie.genre = request.form['genre']
        movie.year = request.form['year']
        movie.musicBy = request.form['musicBy']
        movie.language_id = request.form['language_id']
        movie.youtube_id = request.form['youtube_id']
        movie.ref = request.form['ref']
        movie.yt_thumbnail = 'http://img.youtube.com/vi/'+movie.youtube_id+'/mqdefault.jpg'
        movie.yt_videolink = 'https://www.youtube.com/embed/'+movie.youtube_id
        dbsession.add(movie)
        dbsession.commit()

        return redirect(url_for('movielist', year=movie.year), code=302)

    else:
        return render_template('/movies/edit.html', movie=movie)


@app.route('/telugu/<string:genre>/<int:page>')
def telugu(genre, page):
    genres = dbsession.query(Genre).order_by(Genre.name).all()
    if genre == 'all':
        try:
            movies = Movies.query.filter(and_(Movies.language_id == 2, Movies.youtube_id != None)).paginate(page=page, per_page=20)
        except NoResultFound:
            return redirect("movies")
    else:
        try:
            movies = Movies.query.filter(and_(Movies.language_id == 2, Movies.genre.contains(genre), Movies.youtube_id != None)).paginate(page=page, per_page=20)
        except:
            return redirect("movies")

    return render_template('movies/telugu.html', movies=movies, genres=genres)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
