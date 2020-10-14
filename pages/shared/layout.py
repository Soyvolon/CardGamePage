import dash_html_components as html
from . import navbar as nav

def Layout(content):
    return html.Div([
        nav.Navbar(),
        content
    ])