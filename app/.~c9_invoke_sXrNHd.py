from app import app
from flask import render_template, request, redirect, url_for,send_file,flash
import os
from app import db
from werkzeug import secure_filename
from app.models import Event, User
from .form import eventForm, eventLogin, SignupForm
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug.datastructures import ImmutableOrderedMultiDict

# @app.route('/')
# @app.route('/index')
# def index():
# 	return "Hello, World!"

@app.route('/home')
def home():
	return render_template('home.html', date='March 23, 2016', time='10:00 PM', name='UWI Carnival', location='UWI Mona')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/payment')
def payment():
	return render_template('payment.html')

# @app.route('/details')
# def details():
# 	return render_template('details.html')
	
@app.route('/newevent',methods=['GET','POST'])
def newevent():
    form=eventForm()
    #form=listevent(csrf_enable=False)
    if request.method=='POST':
        img=form.poster.data
        filename=secure_filename(img.filename)
        form.poster.data.save(os.path.join('app/static',filename))
        event=Event(filename,form.eventname.data,form.category.data,form.date.data,form.start_time.data,form.end_time.data,form.venue.data,form.lat.data,form.lng.data,form.capacity.data,form.admission.data,form.description.data,form.contact.data)
        db.session.add(event)
        db.session.commit()
    return render_template('createEvent.html',form=form)
    
 #to be deletedyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
@app.route('/events', methods=['GET','POST'])
def listing():
  elist=db.session.query(Event).all()
  if 1>2:
      lst=[]
      for evnt in elist:
          lst.append({'id':evnt.id,'poster':evnt.poster, 'eventname':evnt.eventname, 'category':evnt.category,'date':evnt.date,'start_time':evnt.start_time,'end_time':evnt.end_time,'venue':evnt.venue,'capacity':evnt.capacity,'admission':evnt.admission,'description':evnt.description,'contact':evnt.contact})
          elist={'elist':lst}
  return render_template('eventspage.html', elist=elist)
#to be deletedyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

@app.route('/events/<cat>', methods=['GET','POST'])
def listings(cat):
  elist=db.session.query(Event).filter_by(category=cat)
  lst=[]
  for evnt in elist:
  		lst.append({'id':evnt.id,'poster':evnt.poster, 'eventname':evnt.eventname, 'category':evnt.category,'date':evnt.date,'start_time':evnt.start_time,'end_time':evnt.end_time,'venue':evnt.venue,'capacity':evnt.capacity,'admission':evnt.admission,'description':evnt.description,'contact':evnt.contact})
  		# elist={'elist':lst}
  return render_template('eventspage.html', elist=elist)

@app.route('/details/<idnum>', methods=['GET','POST'])
def details(idnum):
	ylist=db.session.query(Event).filter_by(id=idnum)
  	lst=[]
  	for evnt in ylist:
  		lst.append({'id':evnt.id,'poster':evnt.poster, 'eventname':evnt.eventname, 'category':evnt.category,'date':evnt.date,'start_time':evnt.start_time,'end_time':evnt.end_time,'venue':evnt.venue,'capacity':evnt.capacity,'admission':evnt.admission,'description':evnt.description,'contact':evnt.contact})
  	return render_template('details.html', ylist=ylist)


@app.route("/")
def landing():
    return render_template('landing.html')
    

@app.errorhandler(404)
    return render_template('landing.html')
	return render_template('404.html'), 404
	

@app.route('/purchase/')
def purchase():
	try:
		return render_template('subscribe.html')
	except Exception, e:
		return 'cant render template'

# @app.route('/login/')
# def login():
# 	form = LoginForm()
# 	if form.validate_on_submit():
request.form.get('username')
# 		user = User.query.filter_by(form.Email=email).first()
# 		if user:
# 			if (user.password==form.password):
# 				loginUser(user)
# 				next = flask.request.args.get('next')
# 				if not next_is_valid(next):
# 					return flask.abort(400)
			
# 		return flask.redirect(next or flask.url_for('index'))
# 	return flask.render_template('login.html', form=form)
	
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login')

@app.route('/signup', methods=['GET','POST'])
def signup():
    form=SignupForm()
    if request.method=='POST':
    	username= request.form[username]
    	email = request.form[email]
    	password = request.form[password]
     	confirm = request.form[confirm]
    	return "{} {} this is".format(username,email,password)
    return render_template('subscribe.html',form=form)   
    
    
    
