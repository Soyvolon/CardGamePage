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
from data import json_converter as jc

import redis

# END IMPORTS ----------------------------
# Utils ------------------------------
def cache_data():
    gr_json = jc.get_data_json(groupdata)
    gu_json = jc.get_data_json(guessdata)

    r.set('groupdata', gr_json)
    r.set('guessdata', gu_json)

def decache_data():
    gr_json = r.get('groupdata')
    gu_json = r.get('guessdata')
    # update the global data
    global groupdata
    global guessdata 
    if(gr_json == None):
        groupdata = DataReader.GetGroupData()
    else:
        groupdata = jc.get_group_list(gr_json)

    if(gu_json == None):
        guessdata = DataReader.GetGuessData()
    else:
        guessdata = jc.get_guess_list(gu_json)
#END Utils ---------------------------

r = redis.Redis(
    host='localhost',
    port=6379
)

groupdata = DataReader.GetGroupData()
guessdata = DataReader.GetGuessData()

cache_data()

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
    decache_data()

    if(pathname == '/cgroup'):
        return GroupData(groupdata)
    elif(pathname == '/cguess'):
        return GuessData(guessdata)
    elif(pathname == '/details'):
        return Details()
    else:
        return Homepage(guessdata, groupdata)

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
    decache_data()
    return jsonify(gr.get_current_game(guessdata, len(groupdata)))

@server.route('/api/v1/game/guess', methods=["POST"])
def guess_respond():
    try:
        if(request.headers['Authorization'] in AuthroizedUsers()):
            json = request.json
            decache_data()
            if du.save_new_guesses(json, guessdata, groupdata):
                cache_data() # save to active cache
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=401)
    except Exception:
        return Response(status=400)

@server.route('/api/v1/game/guess/delete', methods=["POST"])
def guess_delete_respond():
    try:
        if(request.headers['Authroization'] in AuthroizedUsers()):
            json = request.json
            if du.delete_attempt(json, guessdata, groupdata):
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=400)
    except Exception:
        return Response(status=400)

@server.route("/api/v1/game/victory", methods=["POST"])
def victory_respond():
    try:
        if(request.headers['Authorization'] in AuthroizedUsers()):
            json = request.json
            decache_data()
            if du.update_victory(json, guessdata, groupdata):
                cache_data() # save to active cache
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=401)
    except Exception:
        return Response(status=400)

@server.route("/api/v1/game/guess/update", methods=["POST"])
def update_guess_handler():
    try:
        if(request.headers['Authorization'] in AuthroizedUsers()):
            json = request.json
            decache_data()
            if du.update_single_guess(json, guessdata, groupdata):
                cache_data()
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=401)
    except Exception:
        return Response(status=400)

@server.route("/api/v1/game/guess/delete", methods=["POST"])
def delete_guess_handler():
    try:
        if(request.headers['Authorization'] in AuthroizedUsers()):
            json = request.json
            decache_data()
            if du.delete_single_guess(json, guessdata, groupdata):
                cache_data()
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