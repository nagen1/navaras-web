"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify
from navaras import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine, and_
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
            movies = Movies.query.filter(Movies.youtube_id != None).order_by(Movies.title).paginate(page=page, per_page=20)

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
        yt_link = request.form['youtube_id']
        yt_id = yt_link.split("?v=")
        movie.youtube_id = yt_id[1]
        movie.ref = request.form['ref']
        movie.yt_thumbnail = 'http://img.youtube.com/vi/'+yt_id[1]+'/mqdefault.jpg'
        movie.yt_videolink = 'https://www.youtube.com/embed/'+yt_id[1]
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


@app.route('/movies/hindi')
def hindi():
    return render_template('/movies/hindi.html')


@app.route('/movies/tamil')
def tamil():
    return render_template('/movies/tamil.html')

@app.route('/trailers')
def trailers():
    return render_template('/trailers/trailers.html')

@app.route('/tv')
def tv():
    return render_template('/tv/tv.html')

@app.route('/shortfilms')
def shortfilms():
    return render_template('/shortfilms/shortfilms.html')



@app.route('/movies/details/<int:movie_id>')
def moviedetail(movie_id=None):

    try:
        movie = dbsession.query(Movies).filter(Movies.id == movie_id).one()
    except NoResultFound:
        redirect('movies')

    return render_template('movies/details.html', movie=movie)


@app.route('/autocomplete', methods=['GET'])
def autcomplete():
    search = request.args.get('search')

    if search:
        try:
            results = dbsession.query(Movies).filter(and_(Movies.title.like('%'+search+'%'), Movies.youtube_id != None)).limit(10)
            return jsonify(results=[r.serialize for r in results])
        except NoResultFound:
            error = 'No Results found!'
            return render_template('movies/search.html', error=error)


@app.route('/movies/search')
@app.route('/movies/search/<int:page>', methods=['GET', 'POST'])
def search(page=None):
    if request.method == 'POST':
        lookup = request.form['autocomplete']
        if page:
            try:
                movies = Movies.query.filter(and_(Movies.title.like('%'+lookup+'%'), Movies.youtube_id != None)).paginate(page=page, per_page=20)
            except NoResultFound:
                None
        else:
            try:
                movies = Movies.query.filter(Movies.youtube_id != None).paginate(page=1, per_page=20)
            except NoResultFound:
                None
        return render_template('movies/search.html', movies=movies)
    else:
        return redirect('home')


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

''''@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
'''