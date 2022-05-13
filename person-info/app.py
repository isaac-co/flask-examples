from flask import Flask, redirect, render_template, request,  session, redirect
import requests

app = Flask(__name__)
app.secret_key = "key"

def getUserInfo(name):
    gender_res = requests.get(f'https://api.genderize.io/?name={name}')
    age_res = requests.get(f'https://api.agify.io/?name={name}')
    country_res = requests.get(f'https://api.nationalize.io/?name={name}')

    gender = gender_res.json()['gender']
    genderprob = round(gender_res.json()['probability'] * 100, 2)
    age = age_res.json()['age']
    countries = country_res.json()['country']

    return gender, genderprob, age, countries

def getFlag(alpha):
    alpha_res = requests.get(f'https://restcountries.com/v3.1/alpha/{alpha}')
    flag = alpha_res.json()[0]['flag']
    return flag

def getCountryName(alpha):
    alpha_res = requests.get(f'https://restcountries.com/v3.1/alpha/{alpha}')
    common = alpha_res.json()[0]['name']['common']
    return common

def getCountriesInfo(countries):
    countries_names = list()
    flags = list()
    countries_probs = list()
    for country in countries:
        countries_names.append(getCountryName(country['country_id']))
        flags.append(getFlag(country['country_id']))
        countries_probs.append(round(country['probability'] * 100, 2))
    
    return countries_names, flags, countries_probs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info', methods=['POST'])
def info():
    name = request.form.get('name', None)
    gender, genderprob, age, countries = getUserInfo(name)
    countries_names, flags, countries_probs = getCountriesInfo(countries)

    return render_template('info.html', name=name, gender=gender, 
    genderprob=genderprob, age=age, countries_names=countries_names,
    flags=flags, countries_probs=countries_probs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)