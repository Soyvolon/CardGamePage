import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from graphs.guess import current_game, current_guess_counts

def body(guessdata, groupdata):
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Center([
                    html.H2("Data Corner"),
                    html.P(
                        """\
Supporting statistics from the legendary Card Game!
"""
                        ),
                        dbc.Button("View details", color="secondary",
                            href="/details"),
                ]),
            ),
            dbc.Col(html.Center([
                html.H2("Basic Statistics"),
                # composite guess graph goes here
                html.H4("Total Guesses: {total}"
                    .format(total=len(guessdata))
                ),
                html.Br(),
                html.H4("Earliest Date: {edate}"
                    .format(edate=guessdata[0].date)
                ),
                html.H4("Last Date: {ldate}"
                    .format(ldate=guessdata[-1].date)
                )]
            )),
        ]),

        # START Current Game
        dbc.Row([
            dbc.Col(html.Center([
                html.H3("Current Game: #{num}".format(num=len(groupdata)),
                    style={'margin': 5})
            ]))
        ]),
        dbc.Row([
            dbc.Col(html.Center([
                current_game.get_chart(groupdata[-1], "C")
            ]), style={'margin': 5}),
            dbc.Col(html.Center([
                current_game.get_chart(groupdata[-1], "S")
            ]), style={'margin': 5})
        ]),
        dbc.Row([
            dbc.Col(html.Center([
                current_game.get_chart(groupdata[-1], "H")
            ]), style={'margin': 5}),
            dbc.Col(html.Center([
                current_game.get_chart(groupdata[-1], "D")
            ]), style={'margin': 5})
        ]),
        dbc.Row([
            dbc.Col(html.Center([
                current_guess_counts.get_chart(groupdata[-1])
            ]), style={'margin': 5})
        ])
        # END Current Game
        # START Last Game
        
        # END Last Game
    ],
    className="mt-4",
    )

def Homepage(guessdata, groupdata):
    layout = html.Div([
        body(guessdata, groupdata)
    ])

    return layout