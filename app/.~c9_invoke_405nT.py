from app import app
from flask import render_template, request, redirect, url_for, send_file, flash, g
import os
from app import db, login_manager
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from app.models import Event, Users, Comment
from .form import LoginForm, SignupForm, CommentForm, eventForm
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug.datastructures import ImmutableOrderedMultiDict
from app.sentiment_analysis import sentiment
import datetime
from db_insert import *
from functools import wraps

@app.route("/")
def landing():
    return render_template('landing.html')

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
  elist=db.session.query(Event).all()
  if 1>2:
      lst=[]
      for evnt in elist:
          lst.append({'id':evnt.id,'poster':evnt.poster, 'eventname':evnt.eventname, 'category':evnt.category,'date':evnt.date,'start_time':evnt.start_time,'end_time':evnt.end_time,'venue':evnt.venue,'capacity':evnt.capacity,'admission':evnt.admission,'description':evnt.description,'contact':evnt.contact})
          elist={'elist':lst}
  return render_template('home.html', elist=elist)

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/payment')
def payment():
	return render_template('payment.html')

# @app.route('/details')
# def details():
# 	return render_template('details.html')
	
# @app.route('/newevent',methods=['GET','POST'])
# @login_required
# def newevent():
#     form=eventForm()
#     #form=listevent(csrf_enable=False)
#     if request.method=='POST':
#         img=form.poster.data
#         filename=secure_filename(img.filename)
#         insert_event(form.category.data, filename, form.eventname.data, form.date.data, form.start_time.data, form.end_time.data, form.venue.data, form.lat.data, form.lng.data, form.capacity.data,form.admission.data,form.description.data,form.contact.data)
#         form.poster.data.save(os.path.join('app/static/posters',filename))
#     return render_template('createEvent.html',form=form)

    
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
    return Users.query.get(int(id))
    
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = Users.query.filter_by(usersname=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('home'))
    
@app.before_request
def before_request():
    g.user = current_user.get_id()
    
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

    


# @app.route('/signup', methods=['GET','POST'])
# def signup():
#     form = SignupForm()
#     if request.method=='POST':
#         filename = secure_filename(request.form['profile_pic'].filename)
#         insert_user(request.form['first_name'], request.form['last_name'], request.form['usersname'], filename, request.form['email'], request.form['address'], request.form['sex'], request.form['age'], request.form['password'])
        
#         request.form['poster'].save(os.path.join('app/static/profile_pics', filename))
#         return redirect(url_for('choose_category'))
#     return render_template('signup.html')
    
    
@app.route('/choose_category', methods=['GET','POST'])
def choose_category():
    return "TO BE ADDED"
    
@app.route('/comment/<int:id>', methods=['GET','POST'])
def comment(id):
    user_id = g.user
    user = Users.query.filter_by(id=g.user).first()
    username = user.usersname
    event_id = id
    comments = Comment.query.filter_by(event_id=id).all()
    form = CommentForm()
    if request.method == 'GET':
        return render_template('comment.html', username=username,form=form,id=id)
    if form.validate():
        status = sentiment(form.post)[0]
        percentage = str(sentiment(form.post)[1]*100)[:5]
        comment = Comment(user_id,event_id,form.post.data,status,percentage,datetime.datetime.now())
        db.session.add(comment)
        db.session.commit()
        
@app.route('/comments', methods=['GET','POST'])
def comments(id):
    user_id = g.user
    user = Users.query.filter_by(id=g.user).first()
    username = user.usersname
    event_id = request.args.get('id')
    comments = Comment.query.filter_by(event_id=id).all()
    commentz = []
    if request.method=='GET':
        for comment in comments:
            commentz += comment
        return jsonify(comments=commentz)
        
        
        
        
# DO NOT EDIT THIS MY COPY THE ORIGINAL IT ABOVE IF U WANT TO EDIT 
# JUS COMMENT OUT THIS VERSION AND EDIT THE ONE ABOVE
# THIS COPY IS WORKING AND I DO NOT INTEND TO REDO IT

def active_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.status==INACTIVE_USER:
            flash("Please wait for activation")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
    
# @lm.user_loader
# def load_user(id):
#     return User.query.get(int(id))

@app.route('/signup', methods=['GET','POST'])
def signup():
    form=SignupForm()
    if request.method=='POST':
        img=form.profile_pic.data
        filename=secure_filename(img.filename)
        form.profile_pic.data.save(os.path.join('app/static/profile_pics',filename))
        user=Users(form.first_name.data,form.last_name.data,form.username.data,filename,form.email.data,form.password.data,form.address.data,)
        db.session.add(user)
        db.session.commit()
    return render_template('signup.html', form=form)
    
#DO NOT EDIT
@app.route('/newevent',methods=['GET','POST'])
@login_required
@active_required
def newevent():
    form=eventForm()
    #form=listevent(csrf_enable=False)
    if request.method=='POST':
        db.session.commit()
        filename=secure_filename(img.filename)
        form.poster.data.save(os.path.join('app/static/posters',filename))
        event=Event(form.category.data, filename, form.eventname.data, form.date.data, form.start_time.data, form.end_time.data, form.venue.data, form.lat.data, form.lng.data, form.capacity.data,form.admission.data,form.description.data,form.contact.data)
        db.session.add(event)
        db.session.commit()
    return render_template('createEvent.html',form=form)