import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import requests
import endpoint as ep
import os


app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("War",
        style={"textAlign": "center"}),  # Header

        # Button in the center of the screen
        html.Div(
            children=[
                html.Button(
                    "Run Simulation", id="my-button", style={"margin": "auto"}
                )
            ],
            style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "70vh"},
        ),

        html.Div(
            id="output-message",
            children=[],
            style={"text-align": "center"}
        ),


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

@app.callback(
    [Output("p1-score", "children"), 
    Output("p2-score", "children"),
    Output("output-message", "children")],
    [Input("my-button", "n_clicks")]
)
def run_simulation(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    winner = requests.patch("http://127.0.0.1:5000/simulate")
    player1_score = requests.get("http://127.0.0.1:5000/1")
    player2_score = requests.get("http://127.0.0.1:5000/2")

    # print(winner[0])

    return player1_score.text, player2_score.text, winner.text


if __name__ == "__main__":
    app.run_server(debug=True)