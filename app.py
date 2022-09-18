import os
from crypt import methods
from imp import new_module
from typing import MutableSet
from unittest import result
from flask import Flask, render_template, redirect, session, flash, request
from models import connect_db, db, User, Image
from forms import UserForm, SearchForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
import requests, random, math

#####################################
# NEEDED FOR PRODUCTION DEBUGGIN ONLY
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
# toolbar = DebugToolbarExtension(app)
#########################################
# MUST SET UP THE 2 ENVIRON VARS in Terminal - SEE secrets.py

FLASK_KEY = dict(os.environ)["FLASK_KEY"]
API_KEY = dict(os.environ)["API_KEY"]
############################################


if os.environ.get("DATABASE_URL") == None:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "postgresql:///space")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = FLASK_KEY
app.config['API_KEY'] =  API_KEY

connect_db(app)

API_BASE_URL = "https://images-api.nasa.gov"
RV_API_BASE = "https://api.nasa.gov/mars-photos/api/v1"



def collect_API_data(results):
    """Packages data from NASA pictures API"""

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


def calc_rand_sol():
    """Retrieves maximum days of Perseverance on Mars
    and generates a random number within that range
    """

    max_sol_resp =  requests.get(f"{RV_API_BASE}/manifests/perseverance", 
                    params={'api_key': API_KEY})

    if max_sol_resp.status_code != 200:
        flash("Server error encountered. Please try again", "danger")
        return redirect('/') 

    max_sol_data = max_sol_resp.json()
    max_sol = max_sol_data['photo_manifest']['max_sol']
    random_sol = random.randrange(1,int(max_sol))
    return random_sol
    

def check_img_in_db(nasa_id, user):
    """Checks if image is already in DB"""
    images = Image.query.filter(Image.user_id == user.id)
    image_in_db = images.filter(Image.nasa_id == nasa_id).first()
    if image_in_db:
        return True



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
    flash("You have logged out!", "success")
    return redirect('/images')



@app.route('/apod')
def apod():
    """Handles the Astronomy Picture of the Day API"""

    res = requests.get("https://api.nasa.gov/planetary/apod", 
                        params={'api_key': API_KEY})

    if res.status_code != 200:
        flash("Server error encountered. Please try again", "danger")
        return redirect('/') 

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
        
        if res.status_code != 200:
            flash("Server error encountered. Please try again", "danger")
            return redirect('/') 

        data = res.json()
        results = data['collection']['items']
        if not results:
            flash("No results found! Try another search item", "primary")

        result = collect_API_data(results)
        total_hits = data['collection']['metadata']['total_hits']
        
        return render_template('images.html', form=form, result=result, total_hits=total_hits)
        
    return render_template('images.html', form=form)



@app.route('/show_image', methods=['POST'])
def show_image():
    """Displays full size image with details"""

    result = {}
    
    if 'username' in session:
        user = User.query.filter(User.username == session['username']).first()
        username = user.username
        result.update({'username': username})
    else:
        result.update({'username': 'guest'})
    
    nasa_id = request.form.get('nasa_id')

    # retrieving full size image link from API's "asset" endpoint

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



@app.route('/user/<username>/saved_images', methods=['POST'])
def save_image(username):
    """Saves image to DB, if logged in"""

    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.filter(User.username == session['username']).first()
    if user == None:
        raise Unauthorized()

    nasa_id = request.form.get('nasa_id')
    # Checks if image is already in DB
    if check_img_in_db(nasa_id, user):
        flash("Image is already in your list", "warning")
        return redirect('/user/saved_images')

    image = Image(  nasa_id = nasa_id,
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
        flash("Log in to get access!", "danger")
        return redirect('/login')
    user = User.query.filter(User.username == session['username']).first()
    if user == None:
        raise Unauthorized()
    
    return render_template('saved_images.html', user=user)



@app.route('/users/<username>/saved_images/<int:id>/delete', methods=['POST'])
def delete_image(username, id):
    """Deletes an image from DB, if logged in"""

    if 'username' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    if username != session['username']:
        raise Unauthorized()
    image = Image.query.get_or_404(id)
    db.session.delete(image)
    db.session.commit()
    flash("Image deleted!", "success")
    return redirect('/user/saved_images')




@app.route('/rover')
def rover_image():
    """Handles random image from Perseverance rover"""

    random_sol = calc_rand_sol()   

    img_resp = requests.get(f"{RV_API_BASE}/rovers/perseverance/photos", 
                        params={'api_key': API_KEY, 'sol': {random_sol}})

    if img_resp.status_code != 200:
        flash("Server error encountered. Please try again", "danger")
        return redirect('/') 
       
    data = img_resp.json()
    images = data['photos']
    total_hits = len(images)
    if total_hits == 0:
        flash("No images could be retrieved, please try again", "info")
        return redirect ('/images')

    return render_template('rover.html', images=images, total_hits=total_hits, random_sol=random_sol)






