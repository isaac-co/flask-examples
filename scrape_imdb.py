import requests
from bs4 import BeautifulSoup

pelicula = "The Batman"

page = requests.get(f"https://www.imdb.com/search/title/?title={pelicula}")

soup = BeautifulSoup(page.content, "html.parser")

link = soup.find("div", class_="lister-item-content").find("a").get("href")

print(link)

page = requests.get(f"https://www.imdb.com{link}")

soup = BeautifulSoup(page.content, "html.parser")

descripcion = soup.find(attrs={"data-testid": "plot-xl"}).text

imdb_rating = soup.find(class_="sc-7ab21ed2-1 jGRxWM").text

genres = soup.find(attrs={ "data-testid": "genres" }).find_all("li")
genres = [i.text for i in genres]

print(descripcion)
print(imdb_rating)
print(genres)