import dash
import dash_bootstrap_components as dbc

from homepage import Homepage

def run():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    app.layout = Homepage()

    app.run_server(host='0.0.0.0')

if __name__ == "__main__":
    run()