import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from graphs.guess import team_count

def body(data):
    return html.Center(dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H1("Individual Guess Data (From {date})"
                    .format(date=data[0].date)),
                html.Hr()
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H2("Guesses Per Team"),
                dcc.Graph(
                    figure=team_count.get_graph(data)
                )
            ]),
        ]),
    ]))

def GuessData(data):
    return html.Div([
        body(data)
    ])