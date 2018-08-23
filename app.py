from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import phonenumbers
import datetime
import json
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.secret_key = 'a random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kira@localhost/campaign'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Campaign(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    message = db.Column(db.String())
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
    number = db.Column(db.String())
    number_status = db.Column(db.String(20), default='Not Sent')
    status_type = db.Column(db.Integer)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))

    def __init__(self, number, camp_id):
        self.number = number
        self.campaign_id = camp_id

    def __repr__(self):
        return '<Contact %r %r>' %(self.number, self.campaign_id)

@app.route('/')
@app.route('/index')
def index():
    print(db)
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        campaigns = Campaign.query.all()
        return render_template('campaign.html', campaigns = campaigns)

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
    if user:
        session['logged_in'] = True
        campaigns = Campaign.query.all()
        print(campaigns)
        return redirect(url_for('index', campaigns=campaigns))
    else:
        flash('wrong password!')
        return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route('/add')
def add():
    return render_template('add_campaign.html')

@app.route('/valid', methods=['POST'])
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


@app.route('/added', methods=['POST'])
def added():
    camp = Campaign(request.form['title'], request.form['message'], request.form['schedule'])
    db.session.add(camp)
    db.session.commit()
    print(camp.id)

    data = request.form['data']
    data = json.loads(data)
    print(data)

    for item in data:
        # name = item['Name']
        number = item['Number']
        for number in phonenumbers.PhoneNumberMatcher(number, "NP"):
            formatted_number = phonenumbers.format_number(number.number, phonenumbers.PhoneNumberFormat.E164)
            contacts = Contact(formatted_number, camp.id)
            db.session.add(contacts)

    db.session.commit()
    campaigns = Campaign.query.all()
    return redirect(url_for('index', campaigns=campaigns))

@app.route('/getContacts', methods=['POST', 'GET'])
def getContacts():
    id=request.args.get('campaign_details')
    print(id)
    # records = []

    campaign = Campaign.query.filter_by(id=id).all()
    contacts = Contact.query.filter_by(campaign_id=id).all()

    #import ipdb;ipdb.set_trace()
    # for number in camp:
    #     record = number
    #     records.append(record)
        # contacts.number = record
        # db.session.add(contacts)
        # db.session.commit()

    return render_template('contact_details.html',campaign=campaign, contacts = contacts)

@app.route('/duplicate_camp', methods=['POST', 'GET'])
def duplicate_camp():
    campaign_id=request.args.get('campaign_details')
    data = db.session.query(Campaign).filter_by(id=campaign_id).first()
    return render_template('add_campaign.html', Campaign_title = data.title, Campaign_messages = data.message)

@app.route('/dlr', methods=['POST','GET'])
def dlr():
    contact_id = request.args.get('id')
    type = request.args.get('type')
    print('*'*20)
    print(contact_id)
    print(type)
    contact = db.session.query(Contact).filter_by(id=contact_id).first()
    contact.status_type = type
    if type == '1':
        print('type')
        contact.number_status = 'Delivered to phone'
    elif type == '8':
        print('no type')
        contact.number_status = 'Submitted to smsc'

    db.session.add(contact)
    db.session.commit()
    return 'a'

if __name__ == '__main__':
    app.debug=True
    app.run()