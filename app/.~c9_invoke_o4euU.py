from flask.ext.wtf import Form
from wtforms import StringField, TextField, FileField,PasswordField,SubmitField, RadioField, validators
from wtforms.validators import DataRequired, InputRequired, Required, Email, Length, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed


class eventForm(Form):#db.model):
  poster = FileField('poster')
  eventname = TextField('eventname', [DataRequired()])
  category = TextField('category',[DataRequired()])
  date = TextField('date' ,[DataRequired()])
  start_time = TextField('start_time', [Required()])
  end_time = TextField('end_time',[DataRequired()])
  venue = TextField('venue',[DataRequired()])
  lat = TextField('lat',[DataRequired()])
  lng = TextField('lng',[DataRequired()])
  capacity = TextField('capacity',[DataRequired()])
  admission = TextField('admission',[DataRequired()])
  description = TextField('desription',[DataRequired()])
  contact = TextField('contact',[DataRequired()])

class LoginForm(Form):
  email=TextField('username', [DataRequired()])
  password=PasswordField('password', [DataRequired()])

class SignupForm(Form):
  first_name = TextField('first_name', validators=[DataRequired()])
  last_name = TextField('last_name', validators=[DataRequired()])
  username = TextField('usersname', validators=[DataRequired()])
  email = TextField('email', validators=[DataRequired()])
  password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
  confirm = PasswordField('Re-type Password')
  address = TextField('address', validators=[DataRequired()])
  age = TextField('age', validators=[DataRequired()])
  profile_pic = FileField('profile_pic', validators=[FileRequired()])
  sex = RadioField('Sex', choices=[('Male','Male'), ('Female', 'Female')], validators=[InputRequired()])
  
  #This was how I did it in web 2
  # password = PasswordField('password', [validators.Required(), validators.EqualTo('confirm', message='Password mismatched')])
  # confirm = PasswordField('confirm')
  # sex = RadioField('sex', choices=[('Male','Male'), ('Female', 'Female')], validators=[InputRequired()])
    
    
class CommentForm(Form):
  post = StringField('Post', [DataRequired()])
  submit = SubmitField('Post')


class CategoryForm(Form):
  parties
  cultures
  foo
  religious
  