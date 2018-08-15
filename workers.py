import datetime
from app import db, Campaign, Contact
import time
import requests

while 1:
    current_time = datetime.datetime.strptime('2019-06-12T19:30', "%Y-%m-%dT%H:%M")
    campaigns = db.session.query(Campaign).filter_by(schedule=current_time).all()
    for campaign in campaigns:
        print(campaign.id)
        campaign_contacts = db.session.query(Contact).filter_by(campaign_id=campaign.id).all()
        for campaign_contact in campaign_contacts:
            number = campaign_contact.number
            #Call API here
            link = 'http://localhost:13013/cgi-bin/sendsms'
            value = {'username' : 'simple', 'password' : 'simple123', 'from' : 100, 'to' : number, 'text' : 'hello', 'dlr-mask' : 31, 'dlr-url' : 'https://beeceptor.com/console/test314'}
            test = requests.get(link, params=value)
            test.encoding = 'ISO-8859-1'
            print(test)
            print(test.url)

    time.sleep(2)