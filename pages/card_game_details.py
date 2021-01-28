import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def body():
    col = [
            html.Br(),
            html.H1("The Card Game"),
            html.Hr(),
            html.P("""\
\
                """),
            html.H3("The Game"),
            html.P("""\
\
                """),
            html.H3("The Data"),
            html.P("""\
\
                """)
        ]
    
    
    return html.Center(dbc.Container([
        dbc.Row([
            dbc.Col(col)
        ]),
    ]))

def About():
    return html.Div([
        body()
    ])