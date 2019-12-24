#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
import sys
import datetime
from model import app, db, Artist, Shows, Venue
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment = Moment(app)
migrate = Migrate(app, db)
now = datetime.datetime.now()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.all()
  data = []
  addr = {}

  for venue in venues:
      shows = venue.shows
      upcomming = sum(map(lambda x : x.date > now, shows))
      info = {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": upcomming
      }

      if venue.state not in addr:
          addr[venue.state] = {}

      this_state = addr[venue.state]
      if venue.city in this_state:
          this_state[venue.city].append(info)
      else:
          this_state[venue.city] = [info]

  for state in addr:
      for city in addr[state]:
          data.append({
            "city": city,
            "state": state,
            "venues": addr[state][city]
          })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    search = F'%{search_term}%'
    result = Venue.query.filter(Venue.name.like(search)).all()
    data = []

    for one in result:
        shows = one.shows
        upcomming = sum(map(lambda x : x.date > now, shows))
        data.append({
            "id": one.id,
            "name": one.name,
            "num_upcoming_shows": upcomming
        })

    response={
        "count": len(result),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  shows = venue.shows
  upcomming = list(filter(lambda x : x.date > now, shows))
  past = list(filter(lambda x : x.date <= now, shows))
  upcoming_shows = []
  past_shows = []


  for show in upcomming:
      artist = show.artist
      upcoming_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.date)
      })
  for show in past:
      artist = show.artist
      past_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.date)
      })

  data = {
    "id": venue_id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past),
    "upcoming_shows_count": len(upcomming),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
        dict = request.form
        new_venue = Venue(
          name = dict.get('name'),
          city = dict.get('city'),
          state = dict.get('state'),
          address = dict.get('address'),
          phone = dict.get('phone'),
          genres = dict.getlist('genres'),
          facebook_link = dict.get('facebook_link')
        )
        db.session.add(new_venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue could not be deleted.')
    else:
        flash('Venue was successfully deleted!')
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  data = []

  for artist in artists:
      data.append({
        "id": artist.id,
        "name": artist.name
      })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    search = F'%{search_term}%'
    result = Artist.query.filter(Artist.name.like(search)).all()
    data = []

    for one in result:
        shows = one.shows
        upcomming = sum(map(lambda x : x.date > now, shows))
        data.append({
            "id": one.id,
            "name": one.name,
            "num_upcoming_shows": upcomming
        })
    response={
    "count": len(data),
    "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  shows = artist.shows
  upcomming = list(filter(lambda x : x.date > now, shows))
  past = list(filter(lambda x : x.date <= now, shows))
  upcoming_shows = []
  past_shows = []

  for show in upcomming:
      venue = show.venue
      upcoming_shows.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": str(show.date)
      })
  for show in past:
      venue = show.venue
      past_shows.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": str(show.date)
      })
  data={
    "id": artist_id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past),
    "upcoming_shows_count": len(upcomming),
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist_info={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }

  return render_template('forms/edit_artist.html', form=form, artist=artist_info)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    try:
        artist = Artist.query.get(artist_id)
        dict = request.form
        artist.name = dict.get('name'),
        artist.city = dict.get('city'),
        artist.state = dict.get('state'),
        artist.address = dict.get('address'),
        artist.phone = dict.get('phone'),
        artist.genres = dict.getlist('genres'),
        artist.facebook_link = dict.get('facebook_link')
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
    else:
        flash('Artist ' + request.form['name'] + ' was successfully edited!')

    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  venue_info={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }

  return render_template('forms/edit_venue.html', form=form, venue=venue_info)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
      venue = Venue.query.get(venue_id)
      dict = request.form
      venue.name = dict.get('name'),
      venue.city = dict.get('city'),
      venue.state = dict.get('state'),
      venue.address = dict.get('address'),
      venue.phone = dict.get('phone'),
      venue.genres = dict.getlist('genres'),
      venue.facebook_link = dict.get('facebook_link')
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
  else:
      flash('Venue ' + request.form['name'] + ' was successfully edited!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        dict = request.form
        new_artist = Artist(
          name = dict.get('name'),
          city = dict.get('city'),
          state = dict.get('state'),
          phone = dict.get('phone'),
          genres = dict.getlist('genres'),
          facebook_link = dict.get('facebook_link')
        )
        db.session.add(new_artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  shows = Shows.query.all()
  for show in shows:
      artist = show.artist
      venue = show.venue

      data.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.date)
      })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        dict = request.form
        artist = Artist.query.get(dict.get('artist_id'))
        venue = Venue.query.get(dict.get('venue_id'))
        show_date = dict.get('start_time')
        show = Shows(show_date)
        show.venue = venue
        show.artist = artist

        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
    else:
        flash('Show was successfully listed!')

    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
