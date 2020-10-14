import plotly.graph_objects as go

def get_graph(data):
    teams = [x.team for x in data]

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=teams
    ))

    fig.update_layout(
        title_text='Team Guess Counts (From ' + data[0].date + ')',
        xaxis_title='Team',
        yaxis_title='Total Guesses',
        bargap=0.2,
        bargroupgap=0.1,
        xaxis_type='category'
    )

    return fig