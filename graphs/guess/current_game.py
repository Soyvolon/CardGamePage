# pylint: disable=import-error
# pylint failes to resolve graphs.utils.styles locally.

import dash_table
from graphs.utils import styles

headers = [["C", "A"], ["C", "2"], ["C", "3"], ["C", "4"], ["C", "5"], ["C", "6"], ["C", "7"], ["C", "8"], ["C", "9"], ["C", "10"], ["C", "J"], ["C", "Q"], ["C", "K"], ["D", "A"], ["D", "2"], ["D", "3"], ["D", "4"], ["D", "5"], ["D", "6"], ["D", "7"], ["D", "8"], ["D", "9"], ["D", "10"], ["D", "J"], ["D", "Q"], ["D", "K"], ["H", "A"], ["H", "2"], ["H", "3"], ["H", "4"], ["H", "5"], ["H", "6"], ["H", "7"], ["H", "8"], ["H", "9"], ["H", "10"], ["H", "J"], ["H", "Q"], ["H", "K"], ["S", "A"], ["S", "2"], ["S", "3"], ["S", "4"], ["S", "5"], ["S", "6"], ["S", "7"], ["S", "8"], ["S", "9"], ["S", "10"], ["S", "J"], ["S", "Q"], ["S", "K"]]
keys = ["AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS"]

def get_chart(current_game, filter_by_suit = "CHDS"):
    cards = current_game.card_counts

    data = dict(zip(keys, cards))
    kf = []
    cf = []

    for x in data:
        if(x[-1] in filter_by_suit):
            kf.append(x)
            cf.append(data[x])

    data = {"#": current_game.game_id}
    data.update(dict(zip(kf, cf)))

    cols = [{"name": ["", "", "#"], "id": "#"}]
    cols.extend([{"name": i + [i[1] + i[0]], "id": i[1] + i[0] } for i in headers if i[0] in filter_by_suit])

    table = dash_table.DataTable(
        id='current_game_table',
        columns=cols,
        data=[data],
        style_header=styles.header(),
        style_cell=styles.cell(),
        merge_duplicate_headers=True,
        cell_selectable=False,
        style_data_conditional=([
            {
                'if': {
                    'filter_query': '{{{}}} > 0'.format(col),
                    'column_id': col
                },
                'backgroundColor': 'tomato',
            } for col in keys if col != "#"
        ]),
    )

    return table