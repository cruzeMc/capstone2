from . import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('user.id')) #Associated with promoter
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
    admission = db.Column(db.Float) #Now a float type instead of string
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
        
    # def get_id(self):
    #     try:
    #         return unicode(self.id) # python 2 support
    #     except NameError:
    #         return str(self.id) # python 3 support
        
    def __repr__(self):
        return '<Event %r>' % (self.eventname)
        
class User(db.Model): #Changed the name from User's'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(80))
    username = db.Column(db.String(120), index=True)
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), index=True)
    password = db.Column(db.String(80))
    address = db.Column(db.String(120))
    sex = db.Column(db.String(8)) 
    age = db.Column(db.String(20)) #Type changed from integer
    
    def __init__(self, password, first_name, last_name, username, email, address, sex, age):
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
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
            
        @property
        def is_anonymous(self):
            return False
            
        def get_id(self):
            try:
                return unicode(self.id)  # python 2
            except NameError:
                return str(self.id)  # python 3
        
        def __unicode__(self):
        return self.username

# class userLogin(db.model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     username = db.Column(db.String(120), index=True)
#     email = db.Column(db.String(120), index=True)
#     password = db.Column(db.String(80))
    
#     def __init__(self, username, email, password):
#         self.first_name = username
#         self.email = email
#         self.password = password
        
#     @property
#     def is_authenticated(self):
#         return True

#     @property
#     def is_active(self):
#         return True

#     @property
#     def is_anonymous(self):
#         return False

#     def get_id(self):
#         try:
#             return unicode(self.id)  # python 2
#         except NameError:
#             return str(self.id)  # python 3

#     def __repr__(self):
#         return '<User %r>' % (self.username)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = (db.String(80))
    
    
    # def __init__(self, cat_name):
    #     self.cat_name = cat_name
    
    # def __repr__(self):
    #     return '<Event %r' % (self.id)

Selected_Event = db.Table(
    'Selected_Event',
    db.Column('event_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    )

Selected_Category = db.Table(
    'Selected_Category',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('category', db.Integer, db.ForeignKey('category.id'))
    )

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post = db.Column(db.String(160))
    status = db.Column(db.String(8)) #Negative or Positive
    percentage = db.Column(db.String(5)) #percentage
    timestamp = db.Column(db.DateTime)

    
    