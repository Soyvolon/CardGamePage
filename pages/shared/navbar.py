import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Game Data", href="/cgroup")),
            dbc.NavItem(dbc.NavLink("Guess Data", href="/cguess"))    
        ],
        brand="Home",
        brand_href="/",
        sticky="top",
    )
    return navbar