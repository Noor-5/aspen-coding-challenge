'''
Brief: 
This application allows the user to simulate the card game War using a RESTful
API endpoints with a simple user interface. There are two endpoints: one 
runs the play_war() function from the war.py file and updates the database and
the other retrieves the score of a given player ID. The app runs on port
5000 and can be found at http://127.0.0.1:5000/war . Endpoints are run by 
pressing the buttons in the UI.

In order for the app and the endpoints to be hosted on the same flask server, 
both the endpoint and UI code can be found here in the same file. Dash was 
chosen for the UI because of prior experience with it as well as the aility 
it gives to run callbacks on user actions. 
'''

import dash
from dash import dcc, html, ctx
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import requests
from flask import Flask
from flask_cors import CORS, cross_origin
import psycopg2
import configparser
import war as war
from flask import jsonify


server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/war/'
)

config = configparser.ConfigParser()
config.read('config.ini')


app.layout = html.Div(
    children=[
        html.H1("War",
        style={"textAlign": "center"}),  # Header


        # Button to simulate war
        html.Div(
            children=[
                html.Button(
                    "Run Simulation", id="my-button", style={"margin": "auto"}
                )
            ],
            style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "20vh"},
        ),


        html.Div(
            id="output-message",
            children=[],
            style={"text-align": "center"}
        ),

        # Button to reset scores in the database
        html.Div(
            children=[
                html.Button(
                    "Reset Scores", id="reset-score-button", style={"margin": "auto"}
                )
            ],
            style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "40vh"},
        ),

        html.P(id="test", children=[]),

        # Player scores
        html.Div(
            children=[
                html.Div(children=[
                            html.H4("Player 1:"),
                            html.H5(id = "p1-score", children=[])
                        ],
                        id="player-score-left", 
                        className="player-score",
                        style={"float": "left", "margin-left": "20%"}),
                html.Div(children = [
                        html.H4("Player 1:"),
                        html.H5(id = "p2-score", children=[])
                        ],
                        id="player-score-right", 
                        className="player-score", 
                        style={"float": "right", "margin-right": "20%"})
            ],
            style={"text-align": "center", "clear": "both"}
        ),
    ]
)


# Returns db connection usng psycopg2
def get_db_connection():
    conn = psycopg2.connect(
        host=config.get('app', 'db_host'),
        database=config.get('app', 'db_name'),
        user=config.get('app', 'db_user'),
        password= config.get('app', 'db_password'))
    return conn

# Resets scores for layer 1 and player 2 in the db to 0, and returns messages.
def reset_score():
    conn = get_db_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('UPDATE Scores '
        'SET score = 0;')
    cur.close()
    conn.close()
    return "0", "0", "Successfully reset scores!"

# Takes button clicks as input and outputs the scores to each player and
# a message inidicating what happened.
@app.callback(
    [Output("p1-score", "children"), 
    Output("p2-score", "children"),
    Output("output-message", "children")],
    [Input("my-button", "n_clicks"),
    Input("reset-score-button", "n_clicks")],
    prevent_initial_call=True
)
def update_scores(n1, n2):
    # If the simulate button was pressed, run the endpoints
    if "my-button" == ctx.triggered_id:
        winner = requests.patch("http://127.0.0.1:5000/simulate")
        player1_score = requests.get("http://127.0.0.1:5000/1")
        player2_score = requests.get("http://127.0.0.1:5000/2")
        return player1_score.text, player2_score.text, winner.text
    # Reset scores
    elif "reset-score-button" == ctx.triggered_id:
        return reset_score()
    raise PreventUpdate


# Home page with key features.
@server.route("/war")
def my_dash_app():
    return app.index()

# Endpoint to run war simulation. Patch method to update database.
@server.route('/simulate', methods =["PATCH"])
def simulate_war():
    # Run war simulation
    result = war.play_war()
    # Update db by incrementing score of winning player
    try:
        conn = get_db_connection()
        conn.autocommit = True
        cur = conn.cursor()
        tmpl = '''
            UPDATE Scores
            SET score = score + 1
            WHERE playerid = %s
        '''
        cmd = cur.mogrify(tmpl, [result])
        
        cur.execute(cmd)
        cur.close()
        conn.close()
        
        return jsonify(f"Player {result} won!")
    except Exception as e:
        print(e)
        return 
    

# Return the score of the player with the playerid given inputted in the url
# by runnign SELECT query.
@server.route('/<int:playerid>', methods = ["GET"])
def get_score(playerid):
    try:
        conn = get_db_connection()
        conn.autocommit = True
        cur = conn.cursor()
        tmpl = '''
            SELECT score
            FROM Scores
            WHERE playerid = %s
        '''
        
        cmd = cur.mogrify(tmpl, [playerid])
        
        cur.execute(cmd)
        result = jsonify(cur.fetchone())
        cur.close() 
        conn.close()  

        return (result)
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    server.run(port = 5000, debug=True)