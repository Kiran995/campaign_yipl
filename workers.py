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
        # kwargs = {'campaign_id':'campaign.id', 'contact.number_status':'Not Sent'}
        # campaign_contacts = db.session.query(Contact).filter(and_(campaign_id=campaign.id, number_status='Not Sent')).all()
        campaign_contacts = db.session.query(Contact).filter_by(campaign_id=campaign.id).all()
        for campaign_contact in campaign_contacts:
            number = campaign_contact.number
            contact_id = campaign_contact.id
            #Call API here
            link = 'http://localhost:13013/cgi-bin/sendsms'
            value = {'username' : 'simple', 'password' : 'simple123', 'from' : 100, 'to' : number, 'text' : 'hello', 'dlr-mask' : 31, 'dlr-url' : 'http://localhost:5000/dlr/?id={0}&type=%d'.format(contact_id)}
            test = requests.get(link, params=value)
            test.encoding = 'ISO-8859-1'
            campaign.status = 'Sent'
            print(test)
            print(test.url)

    time.sleep(2)