import requests
from requests import ConnectionError


try:
    resp = requests.get('http://localhost:8823')
except requests.ConnectionError:
    print('Could not connect')
