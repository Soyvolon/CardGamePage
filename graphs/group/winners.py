import plotly.graph_objects as go

def get_graph(data):
    fig = go.Figure()
    d = [o.winner for o in data]
    
    fig.add_trace(
        go.Histogram(
            x=d,
        )
    )
    
    fig.update_layout(
        title_text='Card Game Winners (From ' + data[0].start_date + ')',
        xaxis_title='Winner ID',
        yaxis_title='Times Won',
        bargap=0.2,
        bargroupgap=0.1,
        xaxis_type='category'
    )

    return fig