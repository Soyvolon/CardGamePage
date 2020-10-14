import plotly.graph_objects as go

def get_graph(data):
    fig = go.Figure()
    d = [o.total_days for o in data]
    #print(d)

    fig.add_trace(
        go.Box(
            x=d,
            name="Game Length",
    ))

    fig.update_layout(
        title_text='Average Card Game Length (From ' + data[0].start_date + ')',
        xaxis_title="Days"
    )

    return fig