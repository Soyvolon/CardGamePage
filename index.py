import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from pages.homepage import Homepage
from pages.card_group_data_page import GroupData
from pages.card_guess_data_page import GuessData
from pages.shared.layout import Layout
from pages.card_game_details import Details

from flask import request, Response, jsonify
from api.auth import AuthroizedUsers
from api import game_responder as gr
from data import data_updater as du

from data.card_game_data_reader import CardGameDataReader as DataReader

# END IMPORTS ----------------------------

groupdata = DataReader.GetGroupData()
guessdata = DataReader.GetGuessData()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh = False),
    Layout(html.Div(id = 'page-content')),
])

server = app.server

# Callbacks --------------------------

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if(pathname == '/cgroup'):
        return GroupData(groupdata)
    elif(pathname == '/cguess'):
        return GuessData(guessdata)
    elif(pathname == '/details'):
        return Details()
    else:
        return Homepage(guessdata)

# END Callbacks ----------------------
# API Routing ------------------------
@server.route('/api/v1/testauth', methods=["POST"])
def testauth_respond():
    try:
        if(request.headers['Authorization'] in AuthroizedUsers()):
            return Response(status=200)
        else:
            return Response(status=401)
    except Exception:
        return Response(status=400)

@server.route('/api/v1/game/current', methods=["GET"])
def get_current_game_respond():
    return jsonify(gr.get_current_game(guessdata, len(groupdata)))

@server.route('/api/v1/game/guess', methods=["POST"])
def guess_respond():
    try:
        if(request.headers['Authorization'] in AuthroizedUsers()):
            json = request.json
            if du.save_new_guesses(json, guessdata, groupdata):
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=401)
    except Exception:
        return Response(status=400)

@server.route("/api/v1/game/victory", methods=["POST"])
def victory_respond():
    try:
        if(request.headers['Authorization'] in AuthroizedUsers()):
            json = request.json
            if du.update_victory(json, guessdata, groupdata):
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=401)
    except Exception:
        return Response(status=400)

# END API Routing --------------------

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', debug=True)