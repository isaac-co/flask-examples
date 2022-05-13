import requests

from app import anime

def randomActivity():
    res = requests.get('https://www.boredapi.com/api/activity/')
    return res.json()

act = randomActivity()
print(act)
print(act['activity'])


