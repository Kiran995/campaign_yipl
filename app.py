from flask import Flask, render_template
from flask import request, redirect, url_for, flash
import datetime
import os
from werkzeug.utils import secure_filename
import csv
import json

from flask_sqlalchemy import SQLAlchemy
#from app.views import app


UPLOAD_FOLDER = './path/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = 'a random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kira@localhost/postgres'
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Campaign(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80))
    message = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    address = db.relationship('Contact', backref='campaign', lazy=True)

    def __init__(self, title, message, created):
        self.title = title
        self.message = message
        self.created = created


    def __repr__(self):
        return '<Campaign %r>' % self.title

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return '<Contact %r>' %self.number

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.form['username']  == 'admin' and request.form['password'] == 'admin':
        campaigns = Campaign.query.all()
        print('===============================')
        print(campaigns)
        return render_template('campaign.html', campaigns=campaigns)
    else:
        return render_template('login.html')

def allowed_file(filename):
    print(filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['GET','POST'])
def add():
    return render_template('add_campaign.html')

@app.route('/added', methods=['GET','POST'])
def added():
    camp = Campaign(request.form['title'], request.form['message'], request.form['created'])
    db.session.add(camp)
    db.session.commit()
    print(camp.id)


    data = request.form['hidden']
    data = json.loads(data)

    for item in data:
        name = item['Name']
        number = item['Number']

    contact = Contact(number, camp.id)
    db.session.add(contact)
    db.session.commit()

    expected_datetime = request.form['created']
    print(expected_datetime)
    current_datetime = datetime.datetime.now()
    print(current_datetime)
    campaigns = Campaign.query.all()
    return render_template('campaign.html', campaigns=campaigns)

if __name__ == '__main__':
    app.debug=True
    app.run()