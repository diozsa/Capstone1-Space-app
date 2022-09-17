# Capstone1-Space-app

## Title of Project
NASA Visual Exploration - https://iozsa-space-app.herokuapp.com/
## Goal
This app is intended to pique one’s interest about astronomy and increase curiosity about what’s out there - outer Space.
The goal of this app is to offer the users a visual interaction, where simple searches can return amazing photos from NASA public APIs
## Demographics
The app is mainly an educational visual tool, easy to navigate, so that anybody that wants to find out more about Space will be a potential user.
## Features
The site has 4 main parts, accessible through the navbar and uses 3 different APIs:

- NASA Images - a service provided by NASA that allows searches on their image database.
This uses NASA Image Library API - [docs here](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf)
- APOD - Astronomy Picture of the DAY - This micro-API delivers an image/video file updated daily by NASA - [docs here](https://github.com/nasa/apod-api)
- Perseverance Rover - Displays images from Mars. Using this API,  the app randomly selects
a sol (Mars day) out of the total number of days the rover has been active
and retrieves pictures from 15 different cameras - [docs here](https://github.com/chrisccerami/mars-photo-api)
- Your Image Collection - When using the NASA Images search tool
user can add/delete their favorite pictures to/from the database, if they are logged in.
This link is not shown / route is blocked to "Guest" users.
## Used flow
User is taken to the home page that has a brief description of the app. The same page is linked to "About" in the Nav bar.
The 3 services are listed in the Nav bar, and no login is necessary for browsing the site. When user is querying the Nasa Image Library API,
they can select a specific picture which will be routed to a full screen image with title, description, authors, etc. This page has a "Add Image" button.
The database part of the site can only be used by logged in users.<br>
There are friendly messages displayed as action confirmations, also the app checks for response code status and gratiously catches any errors that 
might be coming from the API servers or from interractions with the database.<br>
The logged in username is diplayed in the navbar. "Guest" is displayed if user is not logged in.
## Technology
The site is built in Python3/Flask/Jinja.
## Future addons
Future pagination should be added to the Nasa Image Library page. Currently the API retrieves 100 results per page,
and it defaults to "page=1" as one of the API parameters.<br>
The pagination was intentionally not implemented on the Rover API because the raw data comes in bulk, without description.
There is a lot of repetition in some responses. The image tiles are smaller to fit more on screen
so the easiest way to deal with this is to use the page scroll instead of "Next Page" link.
## Install
- Create a virtual environment with
> python3 -m venv venv
- After cloning, install dependencies from requirements.txt like this:
> pip install -r requirements.txt
*The app was written in Python-3.8.10 - in case you need a specific Python version.*
- ***Make file "secrets.py" in the root folder and add the 2 global variables in this file: API_KEY and FLASK_KEY***
> **Example:**
>> API_KEY = "245gpoi24g029gndfzgg24j"
>> FLASK_KEY = "you_can_choose_whatever_you_want_here"

Both variables are needed at runtime. The API_KEY is also required by 2 of the APIs.<br>
You can quickly and easily get a new API key [here](https://api.nasa.gov) or you can use their DEMO_KEY like this:<br>
> API_KEY = "DEMO_KEY"<br>
>#### The rate limits for the DEMO_KEY are:
>
> - Hourly Limit: 30 requests per IP address per hour
> - Daily Limit: 50 requests per IP address per day
- start Flask server in the terminal with "flask run" command
- go to http://127.0.0.1:5000/