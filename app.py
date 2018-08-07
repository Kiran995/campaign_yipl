from flask import Flask, render_template
from flask import request, redirect, url_for, flash
import datetime
import os
from werkzeug.utils import secure_filename

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
    status = db.Column(db.Boolean, nullable=False, default=False)
    address = db.relationship('Contact', backref='campaign', lazy=True)

    def __init__(self, title, message, created, status):
        self.title = title
        self.message = message
        self.created = created
        self.status = status

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
        print(campaigns)
        return render_template('campaign.html', campaigns=campaigns)
    else:
        return render_template('login.html')

def allowed_file(filename):
    print(filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
    return render_template('add_campaign.html')

@app.route('/added', methods=['POST'])
def added():
    return render_template('campaign.html')

if __name__ == '__main__':
    app.debug=True
    app.run()