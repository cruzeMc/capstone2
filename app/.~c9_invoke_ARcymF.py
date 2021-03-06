from app import app
from flask import render_template, request, redirect, url_for, send_file, flash, g, jsonify
import os
from app import db, login_manager, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from app.models import *
from .form import LoginForm, SignupForm, CommentForm, eventForm, CategoryForm
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug.datastructures import ImmutableOrderedMultiDict
from app.sentiment_analysis import sentiment
import datetime
from db_insert import *
import pdb
from functools import wraps
from operator import itemgetter

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

@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    category_list = db.session.query(Category).all()
    lst = []
    for i in category_list:
        lst.append({'id':i.id, 'category_name':i.category_name, 'image':i.image})
    
    user_id = g.user
    user = db.session.query(Users).filter_by(id=user_id).first()
    form=CategoryForm()
    if request.method == 'POST':
        pdb.set_trace()
        if request.form.get("SPORTS") != None:
            #Users.query.filter_by(id=user_id).first()
            cat1 = Category.query.filter_by(id=8).first()
            user.users_category.append(cat1)
            db.session.commit()
        if request.form.get("PARTIES") != None:
            cat2 = Category.query.filter_by(id=1).first()
            user.users_category.append(cat2)
            db.session.commit()
        if request.form.get("FOODS") != None:
            cat3 = Category.query.filter_by(id=3).first()
            user.users_category.append(cat3)
            db.session.commit()
        if request.form.get("CULTURES") != None:
            cat4 = Category.query.filter_by(id=2).first()
            user.users_category.append(cat4)
            db.session.commit()
        if request.form.get("CHARITY") != None:
            cat5 = Category.query.filter_by(id=6).first()
            user.users_category.append(cat5)
            db.session.commit()
        if request.form.get("COPORATE") != None:
            cat6 = Category.query.filter_by(id=9).first()
            user.users_category.append(cat6)
            db.session.commit()
        if request.form.get("EDUCATION") != None:
            cat7 =Category.query.filter_by(id=7).first()
            user.users_category.append(cat7)
            db.session.commit()
        if request.form.get("RELIGIOUS") != None:
            cat8 = Category.query.filter_by(id=4).first()
            user.users_category.append(cat8)
            db.session.commit()
        if request.form.get("SOCIAL") != None:
            cat9 = Category.query.filter_by(id=5).first()
            user.users_category.append(cat9)
            db.session.commit()
        
        return redirect(url_for('home'))
    
    return render_template('welcome.html', lst=lst)

@app.route('/payment')
def payment():
	return render_template('payment.html')

# @app.route('/details')
# def details():
# 	return render_template('details.html')
	
@app.route('/newevent', methods=['GET','POST'])
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
    comments = Comment.query.filter_by(event_id=event_id).order_by('id desc').all()
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
            return redirect(url_for('welcome'))
    return render_template('signup.html',form=form)
    
@app.route('/rating_sent', methods=['GET', 'POST'])
def rating_sent():
  rating_num = request.args.get('a', None, type=str)
  user_id = g.user
  #Test for number
  try:
      val = int(rating_num)
      if val <= 10:
          return jsonify(result=rating_num)
          
      elif val >= 11:
          e_id = int(str(val)[1:]) # Event ID
          e_num = int(str(val)[0]) # Event Rating
          
          #Update if rating already exist
          if db.session.query(Rating).filter_by(event_id=e_id, users_id=user_id).first():
             id_no = db.session.query(Rating).filter_by(event_id=e_id, users_id=user_id).first()
             new_rating = Rating.query.get(id_no.id)
             new_rating.rate = e_num
             db.session.commit()
             return jsonify(result=rating_num)
          
          else:
              user_rating = Rating(event_id=e_id, users_id=user_id, rate=e_num)
              db.session.add(user_rating)
              db.session.commit()
              return jsonify(result=rating_num)
        
  except ValueError:
      return jsonify(result=rating_num)
  

@app.route('/feed_test', methods=['GET', 'POST'])
def feed_test():
  return render_template('feed_test.html')
    
@app.route('/recommendations', methods=['GET', 'POST'])
def recommend():
    user_id = 1
    recommend_list = []
    users = Users.query.filter_by(id=user_id).first()
    for cat in users.users_category:
        for evnt in cat.events.all():
            recommend_list.append(top_comments(evnt.id))
            
    return recommend_list

def top_comments(event_id):
    events = Event.query.filter_by(id=event_id).all()
    events_dict = {}
    for event in events:
        total_comment = 0.0
        total_rate = 0.0
        total_clicks = 0.0
        comments = Comment.query.filter_by(event_id=event.id).all()
        comments_count = Comment.query.filter_by(event_id=event.id).count()
        ratings = Rating.query.filter_by(event_id=event_id).all()
        ratings_count = Rating.query.filter_by(event_id=event_id).count()
        clicks = Hit.query.filter_by(event_id=event_id).all()
        clicks_count = Hit.query.filter_by(event_id=event_id).count()
        for comment in comments:
            total_comment = total_comment + float(comment.percentage)
        for r in ratings:
            total_rate = total_rate + r.rate
        for click in clicks:
            total_clicks = total_clicks + click.number
        if comments_count!=0:
            total_comment = total_comment/comments_count
        if ratings_count!=0:
            total_rate = total_rate/ratings_count
        if clicks_co
            total_clicks = total_clicks/clicks_count
        events_dict[event.id] = [total
    return events_dict
app.jinja_env.globals.update(top_comments=top_comments)

@app.route('/page_count', methods=['GET', 'POST'])
def page_clicks():
    if request.method=='GET':
        event_id = request.args.get('c', type=str)
        user_id = g.user
        event_hit = Hit.query.filter_by(event_id=event_id,users_id=user_id).first() #its not hits in the db
        if event_hit:
            hits = event_hit.number #its event_hit
            up_hits = int(hits) + 1
            event_hit.number = up_hits
            db.session.add(event_hit)
            db.session.commit()
        else:
            hits = 1
            new_hit = Hit(event_id,user_id,hits)
            db.session.add(new_hit)
            db.session.commit()
	    return event_hit.number
	   
def sum_page_count(event_id):
    event_hit = Hit.query.filter_by(event_id=event_id).all()
    total = 0
    for hits in event_hit:
        total = total + hits.number
    return total
app.jinja_env.globals.update(sum_page_count=sum_page_count)    
    
    