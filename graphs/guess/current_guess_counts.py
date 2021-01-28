# pylint: disable=import-error
# pylint failes to resolve graphs.utils.styles locally.

import dash_table
from graphs.utils.styles import table_css as Css

headers = ["Unique Guesses", "Repeated Guesses", "Total Guesses"]

def get_chart(current_game):
    rawData = [
        current_game.unique_attempts,
        current_game.repeated_guesses,
        current_game.total_attempts
    ]

    data = dict(zip(headers, rawData))

    table = dash_table.DataTable(
        id='current_game_statistics',
        columns=[{"name": i, "id": i } for i in headers],
        data=[data],
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)'
        },
        style_cell={
            'textAlign': 'center',
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'  
        },
        css=Css()
    )

    return table