import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Game Data", href="/game-data")),
            dbc.NavItem(dbc.NavLink("Guess Data", href="/guess-data"))    
        ],
        brand="Home",
        brand_href="/home",
        sticky="top",
    )
    return navbar