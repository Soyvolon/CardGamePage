import dash_table

def get_chart(groupdata):
    
    
    table = dash_table.DataTable(
        id='game_summary_table'
    )

    return table