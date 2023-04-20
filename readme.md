
This is a war simulation app implemented using a Flask localhost server and a Postgres
server. To conifgure the database, change the variables in the config.ini file.

All necessary packages are included in the requirements.txt. Run the following
command to install with pip:
    $ pip install -r requirements.txt

Prior to running the app, initialize the database by runnbing:
    $ python init_db.py

To access the app, run {file name} and go to http://127.0.0.1:5000/war .
Endpoints can be accessed with the following URLs:
    http://127.0.0.1:5000/simulate
    http://127.0.0.1:5000/<playerid> 

Pressing the buttons in the app will call the endpoints, which can be found
within {file name}. The war.py file contains the war simulation code and is 
called by the endpoints. Scores are persisted in the database, but can be reset
by pressing the reset button.

The UI was implemented using Dash, which provides html elements in Python and
callback capabilities. 

Endpoint testing can be found in the endpoint_test.py file.

Given more time, I would have liked to build a more full fledged app following
an MVC framework. Given the application just has one page, I felt that this 
might not be necessary, and I prioritized speed of production. To put both
the endpoint and dash app under the same host, I put the code in the same file,
although I would have prefered modularizing them into different files. Given
more time, I also would have liked to host the application on a server, and 
build out a UI so that the user can visualize each round of the simulated game.
