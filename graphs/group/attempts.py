import plotly.graph_objects as go

def get_graph(data):
    fig = go.Figure()
    unique = []
    total = []
    repeated = []
    #winners = {}
    #colors = []
    for o in data:
        unique.append(o.unique_attempts)
        total.append(o.total_attempts)
        repeated.append(int(o.repeated_guesses))
        #if(not o.winner in winners):
        #    winners[o.winner] = GraphUtils.get_random_color()
        
        #colors.append(winners[o.winner])
    

    fig.add_trace(
        go.Scatter(
            x=unique,
            y=total,
            mode='markers',
            marker=dict(
                size=repeated,
                sizemode='area',
                sizeref=2.*max(repeated)/(80.**2),
                sizemin=4,
                color=repeated,
                showscale=True,
                colorbar=dict(
                    title='Repeated Guesses'
                )
            ),
        )
    )
    
    fig.update_layout(
        title_text='Card Game Guess Data (From ' + data[0].start_date + ')',
        xaxis_title='Unique Guesses',
        yaxis_title='Total Guesses',
    )

    return fig