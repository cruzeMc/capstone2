from flask.ext.wtf import Form
from wtforms import StringField, DecimalField, BooleanField, TextField, FileField, PasswordField, SubmitField, RadioField, IntegerField, SelectField, validators
from wtforms.validators import DataRequired, InputRequired, Required, Email, Length, EqualTo, Email, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import *

c_type = [('','Card Type'), ('visa','Visa'), ('mastercard', 'MasterCard'), ('amex', 'Amex'), ('jcb', 'JCB'), ('discover', 'Discover')]
e_month = [('','Expire Month'), ('01','Jan'), ('02','Feb'), ('03','Mar'), ('04','Apr'), ('05','May'), ('06','June'), ('07','July'), ('08','Aug'), ('09','Sept'), ('10','Oct'), ('11','Nov'), ('12','Dec')]
p_method = [('', 'Payment Method'), ('credit_card','Credit Card'), ('debit_card','Debit Card')]
e_year=[('','Expire year')]
for i in range(2016, 2031):
  e_year.append((str(i), str(i)))

category_names=[("","Select Category")]
category = Category.query.all()
for i in category:
  category_names.append((str(i.id),i.category_name))

class EventForm(Form):
  poster = FileField('Poster')
  eventname = TextField('Event Name', validators=[DataRequired()])
  category = SelectField('Category', choices=category_names, validators=[DataRequired()])
  date = TextField('date')
  start_time = TextField('start_time')
  end_time = TextField('end_time')
  venue = TextField('venue')
  lat = TextField('lat')
  lng = TextField('lng')
  capacity = TextField('capacity')
  admission = TextField('admission')
  description = TextField('desription')
  contact = TextField('contact')
  
class UpdateForm(Form):
  idnum = TextField('id')
  poster = FileField('Poster')
  eventname = TextField('Event Name')
  category = SelectField('Category', choices=category_names)
  date = TextField('date')
  start_time = TextField('start_time')
  end_time = TextField('end_time')
  venue = TextField('venue')
  lat = TextField('lat')
  lng = TextField('lng')
  capacity = TextField('capacity')
  admission = TextField('admission')
  description = TextField('desription')
  contact = TextField('contact')
  

class LoginForm(Form):
  username=TextField('Username', [validators.Required()])
  password=PasswordField('Password', [validators.Required()])
  
  def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

  def validate(self):
      rv = Form.validate(self)
      if not rv:
          return False

      user = Users.query.filter_by(usersname=self.username.data).first()
      if user is None:
          self.username.errors.append('Invalid username')
          return False

      if(user.password!=self.password.data):
          self.password.errors.append('Invalid password')
          return False

      self.user = user
      return True

class SignupForm(Form):
  first_name = TextField('First Name', validators=[DataRequired()])
  last_name = TextField('Last Name', validators=[DataRequired()])
  username = TextField('User Name', validators=[DataRequired(), validators.Required()])
  email = TextField('Email', validators=[DataRequired(), Email(), validators.Required()])
  password = PasswordField('Password', [DataRequired()])
  confirm = PasswordField('Re-type Password', validators=[DataRequired(), validators.EqualTo('password', message='Passwords doesn\'t match')])
  address = TextField('Address', validators=[DataRequired()])
  age = TextField('Age', validators=[DataRequired()])
  profile_pic = FileField('Profile Picture', validators=[FileRequired()])
  sex = RadioField('Sex', choices=[('Male','Male'), ('Female', 'Female')], validators=[InputRequired()])
  utype = SelectField('Account Type', choices=[("","Select Account Type"),("USER","User"),("PROMOTER","Promoter")], validators=[validators.Required(message='Please Select an account Type')])

  def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

  def validate(self):
      rv = Form.validate(self)
      if not rv:
          return False

      user = Users.query.filter_by(usersname=self.username.data).first()
      if user:
          self.username.errors.append('Username already taken')
          return False
    
      email = Users.query.filter_by(email=self.email.data).first()
      if email:
          self.email.errors.append('Account already created with this account')
          return False

      self.user = user
      return True
      
class CommentForm(Form):
  post = StringField('Post', [DataRequired()])
  submit = SubmitField('Post')


#None of these fields would be required since a user decides which they want
class CategoryForm(Form):
  parties = BooleanField('PARTIES')
  cultures = BooleanField('CULTURES')
  foods = BooleanField('FOODS')
  religious = BooleanField('RELIGIOUS')
  sports = BooleanField('SPORTS')
  education = BooleanField('EDUCATION')
  social = BooleanField('SOCIAL')
  charity = BooleanField('CHARITY')
  corporate = BooleanField('CORPORATE')

class CardForm(Form):
  card_num = IntegerField('Card Number', validators=[DataRequired()])
  card_type = SelectField('Card Type', choices=c_type, validators=[validators.Required(message='Please Select a card Type')])
  expire_month = SelectField('Expire Month', choices=e_month, validators=[validators.Required(message='Please select a valid Expiration Month')])
  expire_year = SelectField('Expire Year', choices=e_year, validators=[validators.Required(message='Please select a valid Expiration Year')])
  payment_method = SelectField('Payment Method', choices=p_method, validators=[validators.Required(message='Please select your payment method')])

class PaymentForm(Form):
  card_num = RadioField('Card Number', validators=[InputRequired()])
  event_num = IntegerField('Price', validators=[InputRequired()])
  qty = IntegerField('Quantity', validators=[InputRequired()])

class GetEventForm(Form):
  event_number = IntegerField('Event Numer')