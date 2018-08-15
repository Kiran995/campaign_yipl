import datetime
from app import db, Campaign, Contact
import time
import requests
from sqlalchemy.sql.expression import and_

while 1:
    current_time = datetime.datetime.strptime('2019-06-12T19:30', "%Y-%m-%dT%H:%M")
    campaigns = db.session.query(Campaign).filter_by(schedule=current_time).all()
    for campaign in campaigns:
        print(campaign.id)
        kwargs = {'campaign_id':'campaign.id', 'contact.number_status':'Not Sent'}
        campaign_contacts = db.session.query(Contact).filter(and_(campaign_id=campaign.id, number_status='Not Sent')).all()
        for campaign_contact in campaign_contacts:
            number = campaign_contact.number
            #Call API here
            link = 'http://localhost:13013/cgi-bin/sendsms'
            value = {'username' : 'simple', 'password' : 'simple123', 'from' : 100, 'to' : number, 'text' : 'hello', 'dlr-mask' : 31, 'dlr-url' : 'https://beeceptor.com/console/test314'}
            test = requests.get(link, params=value)
            test.encoding = 'ISO-8859-1'
            print(test)
            print(test.url)
            print(test.headers)
            print(test.json)
            break

    time.sleep(2)