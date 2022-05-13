from flask import Flask, render_template, redirect
from bs4 import BeautifulSoup
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

def randomMovie():
    res = requests.get('https://k2maan-moviehut.herokuapp.com/api/random')
    res = res.json()
    movie = {}
    movie['title'] = res['name']
    movie['year'] = res['releaseYear']
    movie['duration'] = res['runtime']
    movie['genres'] = res['genre']
    movie['rating'] = res['imdbRating']
    movie['score'] = res['metaScore']
    movie['director'] = res['director']
    movie['desc'] = res['overview']
    return movie

def scrapeIMDB(movie_title):
    search = requests.get(f'https://www.imdb.com/search/title/?title={movie_title}')
    soup = BeautifulSoup(search.content, 'html.parser')
    link = soup.find('div', class_='lister-item-content').find('a').get('href')
    page = requests.get(f'https://www.imdb.com{link}')
    soup = BeautifulSoup(page.content, 'html.parser')
    img = soup.find('div', class_='ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width sc-bc5f13ed-0 eCJjuc celwidget ipc-sub-grid-item ipc-sub-grid-item--span-2').find('a').get('href')
    page = requests.get(f'https://www.imdb.com/{img}')
    soup = BeautifulSoup(page.content, 'html.parser')
    img = soup.find('div', class_='sc-7c0a9e7c-2 bkptFa').find('img').get('src')
    return link, img

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
    
@app.route('/movie')
def movie():
    movie = randomMovie()
    link, img = scrapeIMDB(movie['title'])
    movie['link'] = link
    movie['cover'] = img
    print(movie)
    return render_template('movie.html', movie=movie)

@app.route('/game')
def game():
    return redirect('https://word-game-better-than-wordle.herokuapp.com/')

@app.route('/random')
def random_route():
    choices = ['anime','activity','startup','movie','game']
    link = random.choice(choices)
    return redirect(f'/{link}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)