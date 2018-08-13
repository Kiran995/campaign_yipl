from flask import Flask, render_template, session
from flask import request, redirect, url_for, flash
import datetime
import os
import csv
import json
import phonenumbers
from flask_migrate import Migrate
from collections import OrderedDict
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
#from app.views import app


UPLOAD_FOLDER = './path/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = 'a random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kira@localhost/campaign'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Campaign(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80))
    message = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    schedule = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), default='Not Sent')
    address = db.relationship('Contact', backref='campaign')

    def __init__(self, title, message, schedule):
        self.title = title
        self.message = message
        self.schedule = schedule


    def __repr__(self):
        return '<Campaign %r>' % self.title

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))

    def __init__(self, number, camp_id):
        self.number = number
        self.campaign_id = camp_id

    def __repr__(self):
        return '<Contact %r %r>' %(self.number, self.campaign_id)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "You are not logged in. <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def login():
    if request.form['username']  == 'admin' and request.form['password'] == 'admin':
        session['logged_in'] = True
        campaigns = Campaign.query.all()
        print(campaigns)
        return render_template('campaign.html', campaigns=campaigns)
    else:
        flash('wrong password!')
        return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

def allowed_file(filename):
    print(filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['GET','POST'])
def add():
    return render_template('add_campaign.html')

@app.route('/valid', methods=['GET','POST'])
def valid():

    data = request.form['data']
    data = json.loads(data)
    print(data)

    valid_count = 0
    invalid_count = 0
    total_count = 0

    for item in data:
        # name = item['Name']
        number = item['Number']
        total_count = total_count + 1
        for number in phonenumbers.PhoneNumberMatcher(number, "NP"):
            valid_count = valid_count + 1
        print(number)

    invalid_count = total_count - valid_count
    return jsonify({'valid_count': valid_count, 'invalid_count': invalid_count})


@app.route('/added', methods=['GET','POST'])
def added():
    camp = Campaign(request.form['title'], request.form['message'], request.form['schedule'])
    current_datetime = datetime.datetime.now()
    scheduled_datetime = request.form['schedule']
    scheduled_datetime = datetime.datetime.strptime(scheduled_datetime, "%Y-%m-%dT%H:%M")
    if (scheduled_datetime > current_datetime):
        camp.status = 'Queued'
    else:
        camp.status = 'Sent'
    db.session.add(camp)
    db.session.commit()
    print(camp.id)

    data = request.form['data']
    data = json.loads(data)
    print(data)

    for item in data:
        # name = item['Name']
        number = item['Number']
        contacts = Contact(number, camp.id)
        db.session.add(contacts)

    db.session.commit()
    campaigns = Campaign.query.all()
    return render_template('campaign.html', campaigns=campaigns)

@app.route('/getContacts', methods=['POST', 'GET'])
def getContacts():
    id=request.args.get('campaign_details')
    print(id)
    records = []

    for rec in Contact.query.filter_by(campaign_id=id).all():
        record = rec.number
        validity = "invalid"
        for record in phonenumbers.PhoneNumberMatcher(record, "NP"):
            validity = "valid"
        print(rec.number, rec.campaign_id, validity)
        records.append(record)

    return render_template('contact_details.html', contacts=records)

@app.route('/duplicate_camp', methods=['POST', 'GET'])
def duplicate_camp():
    id=request.args.get('campaign_details')
    data = db.session.query(Campaign).filter_by(id=id).first()
    print(id)
    return render_template('add_campaign.html', Campaign_title = data.title, Campaign_messages = data.message)

if __name__ == '__main__':
    app.debug=True
    app.run()