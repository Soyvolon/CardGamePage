import dash_bootstrap_components as dbc
import dash_html_components as html

foot = html.Footer(html.Div(
    className='row',
    children=[
        html.Div(dbc.Button(
            className="btn-outline-info",
            href='https://discord.gg/eHgrBgb',
            target='_blank',
            children=[
                "Discord"
            ]
        ),
        style={
            'align': 'right'
        })
    ],
    style={
        'margin-top': 'auto'
    }
))

def Footer():
    return foot