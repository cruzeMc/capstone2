from . import db, models
import time
import os

def insert_user(first_name2, last_name2, usersname2, filename2, email2, address2, sex2, age2, password2):
    entry = models.Users(first_name=first_name2, last_name=last_name2, usersname=usersname2, pic=filename2, email=email2, address=address2, sex=sex2, age=age2, password=password2)
    db.session.add(entry)
    db.session.commit()

def insert_event(creator2, category2, poster2, eventname2, date2, start_time2, end_time2, venue2, lat2, lng2, capacity2, admission2, description2, contact2):
    event = models.Event(creator=creator2, category=category2, poster=poster2, eventname=eventname2, date=date2, start_time=start_time2, end_time=end_time2, venue=venue2, lat=lat2, lng=lng2, capacity=capacity2, admission=admission2, description=description2, contact=contact2)
    db.session.add(event)
    db.session.commit()