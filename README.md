# Capstone1-Space-app
## Title of Project
NASA Visual Exploration - https://iozsa-space-app.herokuapp.com/
## Goal
This app is intended to pique one’s interest about astronomy and increase curiosity about what’s out there - outer Space.
The goal of this app is to offer the users a visual interaction, where simple searches can return amazing photos from NASA public APIs
## Demographics
The app is mainly an educational visual tool, easy to navigate, so that anybody that wants to find out more about Space will be a potential user.
## Features
The site has 4 main parts and uses 3 different APIs:
    <ul >
        <li>NASA Images - a service provided by NASA that allows 
            searches on their image database. This uses NASA Image Library API - [docs here](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf)
        </li>
        <li>APOD - Astronomy Picture of the DAY - This micro-API delivers an image/video file updated daily by NASA - 
        [docs here](https://github.com/nasa/apod-api)
        </li>
        <li>Perseverance Rover - Displays images from Mars. Using this API,  the app randomly selects
            a sol (Mars day) out of the total number of days the rover has been active
            and retrieves pictures from 15 different cameras [docs here](https://github.com/chrisccerami/mars-photo-api)
        </li>
        <li>
            Your Image Collection - When using the NASA images search tool 
            user can add/delete their favorite pictures to/from the database, if they are logged in. 
        </li>
    </ul>
# Used flow
User is taken to the home page that has a brief description of the app. The same page is linked to "About" in the Nav bar.
The 3 services are listed in the Nav bar, and no login is necessary for browsing the site. When user is querying the Nasa Image Library API,
they can select a specific picture which will be routed to a full screen image with title, description, authors, etc. This page has a Save picture button.
The database part of the site can only be used by logged in users.<br>
There are friendly messages displayed as action confirmations, also the app checks for response code status and gratiously catches any errors that 
might be coming from the API servers or from interractions with the database.<br>
The logged in username is diplayed in the navbar and "Guest" if no user is logged in.
# Technology
The site is built in Python/Flask/Jinja.
# Future addons
Future pagination should be added to the Nasa Image Library service. Currently the API retrieves 100 results per page,
and it defaults to "page=1" as one of the parameters.<br>
The pagination was intentionally not implemented on the Rover API because the raw data comes in bulk, without description.
There is a lot of repetition in some responses. The image tiles are rather small
so the easiest way to deal with this is to use the page scroll instead of "Next Page" link.