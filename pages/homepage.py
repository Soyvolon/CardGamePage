import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def body(data):
    return dbc.Container(
        [
        dbc.Row(
            [
                dbc.Col(
                    html.Center(
                    [
                        html.H2("Data Corner"),
                        html.P(
                            """\
    Supporting statistics from the legendary Card Game!
    """
                            ),
                            dbc.Button("View details", color="secondary",
                                href="/details"),
                    ]),
                    md=4,
                ),
                dbc.Col(html.Center(
                    [
                        html.H2("Basic Statistics"),
                        # composite guess graph goes here
                        html.H4("Total Guesses: {total}"
                            .format(total=len(data))
                        ),
                        html.H4("Current Game #: {games}"
                            .format(games=data[-1].game_id)
                        ),
                        html.Br(),
                        html.H4("Earliest Date: {edate}"
                            .format(edate=data[0].date)
                        ),
                        html.H4("Last Date: {ldate}"
                            .format(ldate=data[-1].date)
                        )
                    ]
                )),
            ]
        )
    ],
    className="mt-4",
    )

def Homepage(data):
    layout = html.Div([
        body(data)
    ])

    return layout