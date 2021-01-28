import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Game Statistics", href="/cgroup")),
            dbc.NavItem(dbc.NavLink("Guess Statistics", href="/cguess"))    
        ],
        brand="Home",
        brand_href="/",
        sticky="top",
        color='primary',
        dark=True
    )
    return navbar