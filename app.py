import os
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
import pyqrcode
from io import BytesIO
import segno

basedir = os.path.abspath(os.path.dirname(__file__))

serverurl = 'https://resdayvoting.aiims.edu'
# create the extension
db = SQLAlchemy()
# create the app
app=Flask(__name__,template_folder='templates')
# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'posters.sqlite')
# initialize the app with the extension
db.init_app(app)
QRcode(app)

class Posters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.String)
    category = db.Column(db.String)
    name = db.Column(db.String)
    dept = db.Column(db.String)
    desig = db.Column(db.String)
    title = db.Column(db.String)
    auth = db.Column(db.String)
    email = db.Column(db.String)



@app.route("/")
def home():
    return render_template("index.html")

@app.route('/posters')
def index():
    posters = Posters.query.all()
    return render_template('posters.html', posters=posters)


@app.route("/posterid/<string:id>")
def poster_detail_by_id(id):
    poster = db.get_or_404(Posters, id)
    return (poster.title)

# https://stackoverflow.com/questions/63226626/how-to-render-an-svg-image-from-an-svg-byte-stream
@app.route("/poster/<string:postercode>")
def poster_detail_by_code(postercode):
    poster = db.one_or_404(db.select(Posters).filter_by(no=postercode))
    fullURL = serverurl + '/poster/' + postercode
    print(fullURL)
    qr = segno.make(fullURL, error='H')
    
    return render_template('vote.html', poster=poster, fullURL=fullURL, qr=qr)


if __name__ == "__main__":
    app.run(debug=True)
