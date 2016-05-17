from . import db
import datetime

ACTIVE_PATRON = 1
PROMOTER = 1
INACTIVE_USER = 0

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('users.id')) #Associated with promoter
    category = db.Column(db.Integer, db.ForeignKey('category.id')) #Now an ID instead-of name
    poster = db.Column(db.String(20))
    eventname = db.Column(db.String(120))
    date = db.Column(db.String(120))
    start_time = db.Column(db.String(80))
    end_time = db.Column(db.String(80))
    venue = db.Column(db.String(80))
    lat = db.Column(db.String(80))
    lng = db.Column(db.String(80))
    capacity = db.Column(db.String(80))
    admission = db.Column(db.String(80)) #Now a float type instead of string
    description = db.Column(db.String(120))
    contact = db.Column(db.String(120))
    
    def __init__(self, creator, category, poster, eventname, date, start_time, end_time, venue, lat, lng, capacity, admission, description, contact):
        self.creator = creator
        self.category = category
        self.poster = poster
        self.eventname = eventname
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.venue = venue
        self.lat = lat
        self.lng = lng
        self.capacity = capacity
        self.admission = admission
        self.description = description
        self.contact = contact
        
    def __repr__(self):
        return '<Event %r>' % (self.eventname)
      
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    usersname = db.Column(db.String(120), index=True)
    pic = db.Column(db.String(80))
    email = db.Column(db.String(120), index=True)
    password = db.Column(db.String(80))
    address = db.Column(db.String(120))
    sex = db.Column(db.String(8))
    age = db.Column(db.String(15))
    comments = db.Colu
    
    # status=db.Column(db.SmallInteger, default=INACTIVE_USER)
    
    def __init__(self, first_name, last_name, usersname, pic, email, address, sex, age, password):
        self.password = password
        self.pic = pic
        self.first_name = first_name
        self.last_name = last_name
        self.usersname = usersname
        self.email = email
        self.address = address
        self.sex = sex
        self.age = age

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
        # return self.status==ACTIVE_PATRON
        
    def active_prom(self):
        return self
    
    @property
    def is_anonymous(self):
        return False
        
    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
            
    def __repr__(self):
        return '<users %r>' % (self.usersname)
        


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category_name = db.Column(db.String(80), nullable=False, index=True)
    image = db.Column(db.String(80), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    post = db.Column(db.String(160))
    status = db.Column(db.String(8)) #Negative or Positive
    percentage = db.Column(db.String(5)) #percentage
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, users_id, event_id, post, status, percentage, timestamp):
        self.users_id = users_id
        self.event_id = event_id
        self.post = post
        self.status = status
        self.percentage = percentage
        self.timestamp = timestamp

event_ratings = db.Table(
    'event_rating',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('rating', db.Integer, nullable=False)
    )

selected_event = db.Table(
    'selected_event',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
    image = d

selected_category = db.Table(
    'selected_category',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('category', db.Integer, db.ForeignKey('category.id'))
    )

#DO NOT EDIT NOR DELETE THIS IS A COPY OF THE ORIGINAL THAT IS COMMENTED OUT ABOVE.
#IF YOU WISH TO EDIT DO NOT CHANGE THIS VERSION JUST COMMENT IT OUT AND UNCOMMENT THE ONE ADOVE THEN EDIT THAT
# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     first_name = db.Column(db.String(80))
#     last_name = db.Column(db.String(80))
#     username = db.Column(db.String(120), index=True)
#     pic = db.Column(db.String(80))
#     email = db.Column(db.String(120), index=True)
#     address = db.Column(db.String(120))
#     password = db.Column(db.String(80))
#     role=db.Column(db.SmallInteger,default=INACTIVE_USER)

#     def __init__(self, first_name, last_name, username, pic, email, address,password):
#         self.password = password
#         self.pic = pic
#         self.first_name = first_name
#         self.last_name = last_name
#         self.username = username
#         self.email = email
#         self.address = address
        
#         @property
#         def is_authenticated(self):
#             return True
        
#         @property
#         def is_active(self):
#             return self.status==ACTIVE_PATRON
            
#         def active_prom(self):
#             return self
        
#         @property
#         def is_anonymous(self):
#             return False
            
#         def get_id(self):
#             try:
#                 return unicode(self.id)  # python 2
#             except NameError:
#                 return str(self.id)  # python 3
        
#         def __repr__(self):
#             return '<Users %r>' % (self.username)