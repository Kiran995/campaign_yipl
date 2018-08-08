from flask import Flask, render_template
from flask import request, redirect, url_for, flash
import datetime
import os
from werkzeug.utils import secure_filename
import csv

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

@app.route('/added', methods=['POST'])
def added():
    error = None

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No files part')
            print("===============")
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash('No files selected')
            print("---------------")
            return redirect(request.url)
        if f and allowed_file(f.filename):
            # f = request.files['file']
            file = secure_filename(f.filename)
            filename = f.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
            print(filename)
            flash('Successfully uploaded file')

    camp = Campaign(request.form['title'], request.form['message'], request.form['created'])
    #contact = Contact(request.form['files'])

    csvfile = request.files['file']
    print(csvfile)
    print('aaaaaaaaaaaaaa')
    # with open('file', newline='') as myFile:
    #     reader = csv.reader(myFile)
    #     for row in reader:
    #         print(row)

    reader = csvfile.read()
    data = list(reader)
    #print(reader)
    for data in reader:
        print("[[[[[[[[[[[[[[[[[[[")
        print(data)

    # csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(reader.splitlines(), skipinitialspace=True)]

    expected_datetime = request.form['created']
    print(expected_datetime)
    current_datetime = datetime.datetime.now()
    print(current_datetime)
    db.session.add(camp)
    db.session.commit()
    campaigns = Campaign.query.all()
    return render_template('campaign.html', campaigns=campaigns)

if __name__ == '__main__':
    app.debug=True
    app.run()