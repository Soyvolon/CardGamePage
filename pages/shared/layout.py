import dash_html_components as html
from . import navbar as nav
from . import footer as foot

def Layout(content):
    return html.Div([
        nav.Navbar(),
        content,
        foot.Footer()
    ])