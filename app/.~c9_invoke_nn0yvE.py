from app import app
from flask import render_template, request, redirect, url_for, send_file, flash, g, jsonify
import os
from app import db, login_manager, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from app.models import *
from .form import LoginForm, SignupForm, CommentForm, eventForm
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug.datastructures import ImmutableOrderedMultiDict
from app.sentiment_analysis import sentiment
import datetime
from db_insert import *
import pdb
from functools import wraps

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route("/")
@app.route("/landing")
def landing():
    category_list = db.session.query(Category).all()
    lst = []
    for i in category_list:
        lst.append({'id':i.id, 'category_name':i.category_name, 'image':i.image})
    return render_template('landing.html', lst=lst)

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
	
@app.route('/newevent',methods=['GET','POST'])
@login_required
def newevent():
    category_list = db.session.query(Category).all()
    lst = []
    for i in category_list:
        lst.append({'id':i.id, 'category_name':i.category_name})
    
    form=eventForm()
    user_id = g.user
    #form=listevent(csrf_enable=False)
    if request.method=='POST':
        img=form.poster.data
        filename=secure_filename(img.filename)
        insert_event(user_id, form.category.data, filename, form.eventname.data, form.date.data, form.start_time.data, form.end_time.data, form.venue.data, form.lat.data, form.lng.data, form.capacity.data,form.admission.data,form.description.data,form.contact.data)
        form.poster.data.save(os.path.join('app/static/posters',filename))
    return render_template('createEvent.html', lst=lst, form=form)

    
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
    user_id = g.user
    user = Users.query.filter_by(id=user_id).first()
    event_id = idnum
    for evnt in ylist:
        lst.append({'id':evnt.id,'poster':evnt.poster, 'eventname':evnt.eventname, 'category':evnt.category,'date':evnt.date,'start_time':evnt.start_time,'end_time':evnt.end_time,'venue':evnt.venue,'capacity':evnt.capacity,'admission':evnt.admission,'description':evnt.description,'contact':evnt.contact})
    return render_template('details.html', ylist=ylist,user_id=user_id,event_id=event_id,user=user)
    
def getUsername(user_id):
    user = Users.query.filter_by(id=user_id).first()
    return [user.usersname,user.pic]
app.jinja_env.globals.update(getUsername=getUsername)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404
	

@app.route('/test', methods=['GET','POST'])
def test():
	return render_template('test.html')

@app.route('/comment_sent', methods=['GET','POST'])
def add_comment():
    post = request.args.get('b', type=str)
    event_id = request.args.get('c', type=str)
    user_id = request.args.get('d', type=str)
    status = sentiment(post)[0]
    percentage = str(sentiment(post)[1]*100)[:5]
    comment = Comment(user_id,event_id,post,status,percentage)
    db.session.add(comment)
    db.session.commit()
    return jsonify(result=post)

@app.route('/comment_recieved')
def get_comments():
    event_id = request.args.get('c', type=str)
    comments = Comment.query.filter_by(event_id=1).all()
    return render_template('comments.html', comments=comments)

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
        err = "Username or Password is invalid"
        return render_template('login.html',err=err)
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
    return redirect(url_for('landing'))


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        file = request.files['profile_pic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            password = form.password.data
            email = form.email.data
            address = form.address.data
            age = form.age.data
            sex = form.sex.data
            new_user = Users(first_name,last_name,username,filename,email,address,sex,age,password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html',form=form)



@app.route('/details_test/<idnum>', methods=['GET','POST'])
def details_test(idnum):
    ylist=db.session.query(Event).filter_by(id=idnum)
    lst=[]
    user_id = g.user
    user = Users.query.filter_by(id=user_id).first()
    event_id = idnum
    comments = Comment.query.filter_by(event_id=event_id).all()
    for evnt in ylist:
        lst.append({'id':evnt.id,'poster':evnt.poster, 'eventname':evnt.eventname, 'category':evnt.category,'date':evnt.date,'start_time':evnt.start_time,'end_time':evnt.end_time,'venue':evnt.venue,'capacity':evnt.capacity,'admission':evnt.admission,'description':evnt.description,'contact':evnt.contact})
    if request.method == "POST":
        status = sentiment(request.form['post'])[0]
        percentage = str(sentiment(request.form['post'])[1]*100)[:5]
        comment = Comment(user_id,event_id,request.form['post'],status,percentage)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('details_test', idnum=idnum))
    return render_template('details2.html', ylist=ylist,comments=comments,user=user)
    
@app.route('/rating_sent', methods=['GET', 'POST'])
def rating_sent():
  rating_num = request.args.get('a', None, type=str)
  user_id = g.user
  
  #Test for number
  try:
      #pdb.set_trace()
      val = int(rating_num)
      if val <= 10:
          return jsonify(result=rating_num)
          
      elif val >= 11:
          e_id = int(str(val)[1:])
          e_num = int(str(val)[0])
          
          #Update if rating alread exist
          if db.session.query(Rating).filter_by(users_id=user_id, event_id=e_id).first():
              db.session.query(Rating).filter_by(users_id=user_id, event_id=e_id).update({'rate': e_num})
              db.session.commit()
  except ValueError:
      return jsonify(result=rating_num)
  
  #Add new rating
  val = int(rating_num)
  e_id = int(str(val)[1:])
  e_num = int(str(val)[0])
  #pdb.set_trace()
  #pdb.set_trace()
  db.session.add(user_rating)
  db.session.commit()
  return jsonify(result=rating_num)

@app.route('/feed_test', methods=['GET', 'POST'])
def feed_test():
  return render_template('feed_test.html')
    
    
    
@app.route('/choose_category', methods=['GET','POST'])
def choose_category():
    return "TO BE ADDED"
    
        
