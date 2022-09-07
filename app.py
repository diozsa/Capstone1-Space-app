from crypt import methods
from imp import new_module
from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
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

API_BASE_URL = "https://images-api.nasa.gov/"



def collect_data(results):
    """Package data from API"""

    result = []
    for item in results:
        nasa_id = item['data'][0].get('nasa_id')
        title = item['data'][0].get('title')
        description = item['data'][0].get('description')
        thumbnail = item['links'][0].get('href')
        photographer = item['data'][0].get('photographer')
        creator = item['data'][0].get('secondary_creator')
        result.append({'nasa_id': nasa_id, 'title': title, 'description': description, 'thumbnail': thumbnail, 'photographer': photographer, 'creator': creator})
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
        return redirect('/')
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
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    """Log out route"""

    session.pop('username')
    flash("See you soon!", "info")
    return redirect('/')

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
    """Shows images based on data from the API"""

# data['collection']['items'][record#]['data'][0]['title']
    
    form = SearchForm()
    
    if form.validate_on_submit():
        search = form.search.data
        res = requests.get(f"{API_BASE_URL}/search", 
                            params={'q': search, 'media_type': 'image'})
        data = res.json()
        results = data['collection']['items']
        if not results:
            flash("No results found!", "primary")

        result = collect_data(results)
        total_hits = data['collection']['metadata']['total_hits']
        
        return render_template('images.html', form=form, result=result, total_hits=total_hits)
        
    return render_template('images.html', form=form)


