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

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True)