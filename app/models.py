from . import db
import datetime

ACTIVE_PATRON = 1
PROMOTER = 1
INACTIVE_USER = 0

selected_event = db.Table(
    'selected_event',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
    )

selected_category = db.Table(
    'selected_category',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('category', db.Integer, db.ForeignKey('category.id'))
    )

card_association = db.Table(
    'card_association',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('card_id', db.BIGINT, db.ForeignKey('card.id'))
    )

# selected_rating = db.Table(
#     'selected_rating',
#     db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
#     db.Column('rate', db.Integer)
#     )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category_name = db.Column(db.String(80), nullable=False, index=True)
    image = db.Column(db.String(80), nullable=False)
    
    categories = db.relationship('Users', secondary=selected_category, backref=db.backref('users_category', lazy='dynamic')) #Many to many
    events = db.relationship('Event', backref='category_event', lazy='dynamic') #One to Many

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('users.id')) #Associated with promoter
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True) #Can exist without a category
    poster = db.Column(db.String(120))
    eventname = db.Column(db.String(120))
    date = db.Column(db.String(120))
    start_time = db.Column(db.String(80))
    end_time = db.Column(db.String(80))
    venue = db.Column(db.String(80))
    lat = db.Column(db.String(80))
    lng = db.Column(db.String(80))
    capacity = db.Column(db.Integer)
    admission = db.Column(db.Numeric(10, 2))
    description = db.Column(db.String(120))
    contact = db.Column(db.Integer)#this shouldnt be restricter to an integer. it should be a string in the case of the user entering an email address.

    #Separate for readability purpose
    comments = db.relationship('Comment', backref='event_comment', lazy='dynamic') #One to many
    ratings = db.relationship('Rating', backref='event_rating', lazy='dynamic')
    hit = db.relationship('Hit', backref='event_hit', lazy='dynamic')
    payments = db.relationship('Payment', backref='event_payment', lazy='dynamic')
    
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
    age = db.Column(db.String(30))
    urole = db.Column(db.String(8))
    
    comments = db.relationship('Comment', backref='users_comment', lazy='dynamic')
    events = db.relationship('Event', secondary=selected_event, backref=db.backref('users_event', lazy='dynamic'))
    cards = db.relationship('Card', secondary=card_association, backref=db.backref('users_card', lazy='dynamic'))
    payments = db.relationship('Payment', backref='users_payment', lazy='dynamic')
    
    def __init__(self, first_name, last_name, usersname, pic, email, address, sex, age, password,urole):
        self.password = password
        self.pic = pic
        self.first_name = first_name
        self.last_name = last_name
        self.usersname = usersname
        self.email = email
        self.address = address
        self.sex = sex
        self.urole = urole
        self.age = age
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
        
    def active_prom(self):
        return self
    
    @property
    def is_anonymous(self):
        return False
        
    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 
            
    def get_urole(self):
        return self.urole
            
    def __repr__(self):
        return '<users %r>' % (self.usersname)
        

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    users_id = db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
    post = db.Column(db.String(160))
    status = db.Column(db.String(8)) #Negative or Positive
    percentage = db.Column(db.String(8)) #percentage
    timestamp = db.Column(db.DateTime)

    def __init__(self, users_id, event_id, post, status, percentage):
        self.users_id = users_id
        self.event_id = event_id
        self.post = post
        self.status = status
        self.percentage = percentage
        self.timestamp = datetime.datetime.now()
        
    def __repr__(self):
        return '<Comment %r>' % (self.users_id)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
    users_id = db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
    rate = db.Column(db.Integer, nullable=False)
    
    def __init__(self, event_id, users_id, rate):
        self.event_id = event_id
        self.users_id = users_id
        self.rate = rate
         
    def __repr__(self):
        return '<Rating %r>' % (self.rate)

class Hit(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
    users_id = db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
    number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Date)
    
    def __init__(self, event_id, users_id, number):
        self.event_id = event_id
        self.users_id = users_id
        self.number = 1
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        
    def __repr__(self):
        return '<Hit %r>' % (self.number)

class Card(db.Model):
    id = db.Column(db.BIGINT, primary_key=True, nullable=False) #Card Number
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    card_cvv = db.Column(db.Integer)
    card_type = db.Column(db.String(12))
    expire_month = db.Column(db.String(10))
    expire_year = db.Column(db.Integer)
    payment_method = db.Column(db.String(20))
    
    
    def __init__(self, id, card_cvv, card_type, expire_month, expire_year, user_id, payment_method):
        self.id = id
        self.card_cvv = card_cvv
        self.card_type = card_type
        self.expire_month = expire_month
        self.expire_year = expire_year
        self.user_id = user_id
        self.payment_method = payment_method
    
    def __repr__(self):
        return '<Card number %r>' % (self.id)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    users_id = db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
    card_num = db.Column(db.BIGINT)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    
    def __init__(self, users_id, event_id,  card_num, price, quantity):
        self.users_id = users_id
        self.event_id = event_id
        self.card_num = card_num
        self.price = price
        self.quantity = quantity
    
    def __repr__(self):
        return '<Transaction amount %r>' % (self.price * self.quantity)