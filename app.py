from crypt import methods
from imp import new_module
from unittest import result
from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Image
from forms import UserForm, DeleteForm, SearchForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
import requests
from secrets import API_KEY, FLASK_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///space"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = FLASK_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

API_BASE_URL = "https://images-api.nasa.gov"



def collect_API_data(results):
    """Package data from API"""

    result = []
    for item in results:
        nasa_id = item['data'][0].get('nasa_id')
        title = item['data'][0].get('title')
        description = item['data'][0].get('description')
        photographer = item['data'][0].get('photographer')
        creator = item['data'][0].get('secondary_creator')
        thumbnail = item['links'][0].get('href')


        result.append({ 'nasa_id': nasa_id,
                        'title': title,
                        'description': description,
                        'photographer': photographer,
                        'creator': creator,
                        'thumbnail': thumbnail})

    return result
    


##############  404 ROUTE  ################

@app.errorhandler(404)
def page_not_found(e):
    """Shows CUSTOM page not found """
    return render_template('404.html')


############### HOME ROUTE #################
#     
@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Generates and handles the user form
        for registering a new user
    """
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)
        
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username already taken.  Try another username.')
            return render_template('register.html', form=form)
        
        session['username'] = new_user.username
   
        flash('Account created successfully!', "success")
        return redirect('/images')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Logs in user using the User Form"""

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f'Welcome back, {user.username}!', "primary")
            session['username'] = user.username
            # do_login(user)
            
            return redirect('/images')
        else:
            form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    """Log out route"""

    session.pop('username')
    # do_logout()
    flash("You have logged out!", "info")
    return redirect('/images')

# check incoming data by base URL in order to know 
# what fields are coming

@app.route('/apod')
def apod():
    """Handles the Astronomy Picture of the Day API"""

    res = requests.get("https://api.nasa.gov/planetary/apod", 
                        params={'api_key': API_KEY})
    data = res.json()
    return render_template('apod.html', data=data)


@app.route('/images', methods=['GET', 'POST'])
def show_images():
    """Shows images requested from the API"""

    
    form = SearchForm()
    
    if form.validate_on_submit():
        search = form.search.data
        res = requests.get(f"{API_BASE_URL}/search", 
                            params={'q': search, 'media_type': 'image'})
        data = res.json()
        results = data['collection']['items']
        if not results:
            flash("No results found!", "primary")

        result = collect_API_data(results)
        total_hits = data['collection']['metadata']['total_hits']
        
        return render_template('images.html', form=form, result=result, total_hits=total_hits)
        
    return render_template('images.html', form=form)



@app.route('/show_image', methods=['POST'])
def show_image():
    """Displays full size image with details"""

    result = {}
    # nasa_id = request.form.get('nasa_id')
    # title = request.form.get('title')
    # description = request.form.get('description')
    # photographer = request.form.get('photographer')
    # creator = request.form.get('creator')
    # thumbnail = request.form.get('thumbnail')

    # # retrieving full size image from "asset" endpoint
    # image_url = requests.get(f"{API_BASE_URL}/asset/{nasa_id}")
    # image_url = image_url.json() 

    # result.update({ 'nasa_id': nasa_id,
    #                 'title': title,
    #                 'description': description,
    #                 'photographer': photographer,
    #                 'creator': creator,
    #                 'thumbnail': thumbnail,
    #                 'full_image': image_url['collection']['items'][0]['href']})
    nasa_id = request.form.get('nasa_id')

    # retrieving full size image from "asset" endpoint
    image_url = requests.get(f"{API_BASE_URL}/asset/{nasa_id}")
    image_url = image_url.json() 

    result.update({ 'nasa_id': nasa_id,
                    'title': request.form.get('title'),
                    'description': request.form.get('description'),
                    'photographer': request.form.get('photographer'),
                    'creator': request.form.get('creator'),
                    'thumbnail': request.form.get('thumbnail'),
                    'full_size': image_url['collection']['items'][0]['href']})
    
    
    return render_template('show_img.html', result=result)



@app.route('/user/saved_images', methods=['POST'])
def save_image():
    """Saves image to DB"""

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    user = User.query.filter(User.username == session['username']).first()

    # user_id = user.id
    # nasa_id = request.form.get('nasa_id')
    # title = request.form.get('title')
    # description = request.form.get('description')
    # photographer = request.form.get('photographer')
    # creator = request.form.get('creator')
    # thumbnail = request.form.get('thumbnail')

    image = Image(  img_id = request.form.get('nasa_id'),
                    title = request.form.get('title'),
                    description = request.form.get('description'),
                    photographer = request.form.get('photographer'),
                    creator = request.form.get('creator'),
                    thumbnail = request.form.get('thumbnail'),
                    full_size = request.form.get('full_size'),
                    user_id = user.id
                    )
    
    db.session.add(image)
    db.session.commit()
    flash('Image added to your collection!', 'success')
    return redirect('/images')


@app.route('/user/saved_images')
def show_saved_images():
    """Displays all saved images"""

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    user = User.query.filter(User.username == session['username']).first()

    user = User.query.get(username)
    form = DeleteForm()
    return render_template('saved_images')
