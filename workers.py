import datetime
from app import db, Campaign, Contact
import time
import requests
from sqlalchemy.sql.expression import and_

while 1:
    print('s')
    # import ipdb;ipdb.set_trace()
    current_time = datetime.datetime.now()
    print(current_time)
    campaigns = db.session.query(Campaign).filter(and_(Campaign.schedule <= current_time, Campaign.status == 'Not Sent')).all()
    print(campaigns)
    for campaign in campaigns:
        print(campaign.id)
        campaign_contacts = db.session.query(Contact).filter_by(campaign_id = campaign.id).all()
        for campaign_contact in campaign_contacts:
            number = campaign_contact.number
            contact_id = campaign_contact.id
            link = 'http://localhost:13013/cgi-bin/sendsms'
            value = {'username' : 'simple', 'password' : 'simple123', 'from' : 100, 'to' : number, 'text' : 'hello', 'dlr-mask' : 31, 'dlr-url' : 'http://localhost:5000/dlr?id={0}&type=%d'.format(contact_id)}
            test = requests.get(link, params=value)
            test.encoding = 'ISO-8859-1'
            campaign.status = 'Sent'
            db.session.add(campaign)
            db.session.commit()

    time.sleep(2)