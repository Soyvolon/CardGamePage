import dash
import dash_bootstrap_components as dbc

from homepage import Homepage

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = Homepage()

server = app.server

if __name__ == "__main__":
    app.run_server(host='0.0.0.0')