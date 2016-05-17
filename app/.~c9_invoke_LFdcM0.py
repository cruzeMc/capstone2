from app import app
from flask import render_template, request, redirect, url_for, send_file, flash, g
import os
from app import db, login_manager
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from app.models import Event, User
from .form import LoginForm, SignupForm, eventForm
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
        event=Event(filename,form.category.data, form.eventname.data,form.date.data,form.start_time.data,form.end_time.data,form.venue.data,form.lat.data,form.lng.data,form.capacity.data,form.admission.data,form.description.data,form.contact.data)
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
def page_not_found(error):
	return render_template('404.html'), 404
	

@app.route('/purchase')
def purchase():
	try:
		return render_template('subscribe.html')
	except Exception, e:
		return 'cant render template'

@login_manager.user_loader
def load_user(id):
    return login_user.query.get(int(id))
    
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('home'))
    
@app.before_request
def before_request():
    g.user = current_user
    
# def login():
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 	    username = request.args.get('username', '', type=str)
# 	    password = request.args.get('password', '', type=str)
# 	    user = User.query.filter_by(username=username).first()
# 	    if user:
# 	        if (user.password==form.password):
# 	            loginUser(user)
# 	            next = flask.request.args.get('next')
	            
# 	            if not next_is_valid(next):
# 	                return flask.abort(400)
	            
# 	            else:
# 	                return flask.redirect(next or flask.url_for('home'))
# 	        else:
# 	            return "Invalid Password"
# 		 else:
# 		     return "Invalid Username"
# 	return flask.render_template('login.html', form=form)
	
@app.route("/logout")
@login_required
def logout():     
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    form=SignupForm()
    if request.method=='GET':
        return rnder_template('signup.html'
        
        user = User(request.form['password'],request.form['first_name'],,request.form['last_name,request.form[''],
                    ,request.form[''],,request.form[''],
    	username= request.form['username']
    	email = request.form['email']
    	password = request.form['password']
     	confirm = request.form['confirm']
#   	return "{} {} this is".format(username,email,password)
    return render_template('subscribe.html',form=form)   
    
    
    
