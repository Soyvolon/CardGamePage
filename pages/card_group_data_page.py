import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from graphs.group import game_length, attempts, winners

def body(data):
    return html.Center(dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H1("Card Game Data (From {date})"
                    .format(date=data[0].start_date)),
                html.Hr()
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H2("Average Game Length"),
                dcc.Graph(
                    figure=game_length.get_graph(data)
                )
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H2("Game Winners"),
                dcc.Graph(
                    figure=winners.get_graph(data)
                )
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H3("Individual Guess Data"),
                dcc.Graph(
                    figure=attempts.get_graph(data)
                )
            ])
        ])
    ]))

def GroupData(data):
    return html.Div([
        body(data)
    ])