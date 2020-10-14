# auth.json is a basic json list [ "" ] where
# each item is an Authroization header for Basic Auth
# ex: [ "Basic Og==" ] would be a basic auth with no
# username or password inputed.

import json
import os

path = os.path.join(os.path.dirname(__file__), 'auth.json')
with open(path, 'r') as auth_file:
    auth = json.load(auth_file)

def AuthroizedUsers():
    return auth

if(__name__ == "__main__"):
    print(auth)