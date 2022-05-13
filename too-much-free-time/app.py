from flask import Flask, render_template, redirect
import requests
import random

def randomAnime():
    res = requests.get('https://api.aniapi.com/v1/random/anime/1/true')
    anime_info = {}
    try:
        anime_info['mal_id'] = res.json()['data'][0]['mal_id']
    except KeyError:
        anime_info['mal_id'] = 0
    anime_info['rj_title'] = res.json()['data'][0]['titles']['rj']
    anime_info['jap_title'] = res.json()['data'][0]['titles']['jp']
    anime_info['en_title'] = res.json()['data'][0]['titles']['en']
    anime_info['eps'] = res.json()['data'][0]['episodes_count']
    anime_info['cover'] = res.json()['data'][0]['cover_image']
    anime_info['genres'] = ', '.join(res.json()['data'][0]['genres'])
    anime_info['nsfw'] = res.json()['data'][0]['nsfw']
    anime_info['desc'] = res.json()['data'][0]['descriptions']['en']
    if not anime_info['desc'] is None:
        anime_info['desc'] = res.json()['data'][0]['descriptions']['en'].replace('<br>', "")
    return anime_info

def randomActivity():
    res = requests.get('https://www.boredapi.com/api/activity/')
    return res.json()

app = Flask(__name__)
app.secret_key = "key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/anime')
def anime():
    anime_info = randomAnime()
    return render_template('anime.html', anime=anime_info)

@app.route('/activity')
def activity():
    act = randomActivity()
    return render_template('random.html', act=act)

@app.route('/startup')
def startup():
    act = {}
    res = requests.get('https://itsthisforthat.com/api.php?text').text
    act['activity'] = res
    return render_template('random.html', act=act)
    
@app.route('/cocktail')
def cocktail():
    return redirect('https://www.thecocktaildb.com/api/json/v1/1/random.php')

@app.route('/random')
def random_route():
    choices = ['anime','activity','startup','cocktail']
    link = random.choice(choices)
    return redirect(f'/{link}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)