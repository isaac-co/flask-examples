import requests

page = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")

if page.status_code == 200:
    contenido = page.json()
    print(contenido["id"])
    print(contenido["base_experience"])
    print(contenido["height"])
    print(contenido["weight"])
    abilities = contenido["abilities"]
    for i in abilities:
        print(i["ability"]["name"])
    print(contenido["sprites"]["front_default"])
    print(contenido["sprites"]["back_default"])