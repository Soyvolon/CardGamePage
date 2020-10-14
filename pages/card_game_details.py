import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def body():
    return html.Center(dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H1("The Card Game"),
                html.Hr()
            ])
        ]),
    ]))

def Details():
    return html.Div([
        body()
    ])