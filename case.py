from flask import Flask, request, make_response, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import string
import random
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from functions import check_short, check_short2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

db = SQLAlchemy(app)


class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True) #Name, type of column
    url = db.Column("url", db.String())     #store url URLS
    shortcode = db.Column("shortcode", db.String(6), unique=True)  #store shortcodes URLS, limit of 6 characters
    created_date = db.Column("created_date", db.String())
    last_redirect = db.Column("last_redirect", db.String())
    redirect_count = db.Column("redirect_count", db.Integer())


def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_"
    rand_letters = random.choices(letters, k=6)
    rand_letters = "".join(rand_letters)         # Convert the list of letters into a string of 6 letters.
    return rand_letters


@app.route('/shorten', methods=['POST'])
def add_url():
    if request.method == 'POST':
        url = request.get_json(force=True).get('url', None)
        shortcode = request.get_json(force=True).get('shortcode', None)

        if shortcode == None:
            shortcode = shorten_url()
        if check_short(shortcode) == False:
            response = make_response(jsonify({'message': 'The provided shortcode is invalid'}), 412)
            return response
        if url == None:
            response = make_response(jsonify({'message': 'Url not present'}), 400)
            return response
        if url.startswith('https://') == False:
            response = make_response(jsonify({'message': 'The provided url is invalid'}), 412)
            return response

        now = datetime.now()
        created_date = str(now)
        redirect_count = 0
        last_redirect = ''
        url1 = Urls(url=url, shortcode=shortcode, created_date=created_date, last_redirect=last_redirect,
                    redirect_count=redirect_count)

        try:
            db.session.add(url1)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            response = make_response(jsonify({'message': 'Shortcode already in use'}), 404)
            return response

    return make_response(jsonify({'shortcode': shortcode}), 201)


@app.route('/<shortcode>', methods=['GET'])
def get_url(shortcode):
    db_row = Urls.query.filter_by(shortcode=shortcode).first()
    if check_short2(db_row) == False:
        response = make_response(jsonify({'message': 'Shortcode not found'}), 404)
        return response
    db_row.redirect_count += 1
    now = datetime.now()
    db_row.last_redirect = str(now)
    db.session.commit()
    return redirect(db_row.url, 302)


@app.route('/<shortcode>/stats', methods=['GET'])
def get_stats(shortcode):
    db_row = Urls.query.filter_by(shortcode=shortcode).first()
    if check_short2(db_row) == False:
        response = make_response(jsonify({'message': 'Shortcode not found'}), 404)
        return response
    return make_response(jsonify({'lastRedirect': db_row.last_redirect, 'RedirectCount': db_row.redirect_count,
                                  'createdDate': db_row.created_date}), 200)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
