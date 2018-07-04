from pprint import pprint
import shutil

import bs4
import requests

base_url = "http://mangalife.us"
url = "http://mangalife.us/manga/Boku-No-Hero-Academia"
html = requests.get(url).text
soup = bs4.BeautifulSoup( html , "html.parser")
classes = []
chapter_links = [chapter["href"] for chapter in soup.select(".list-group-item")]

page = requests.get(base_url + chapter_links[-1]).text
chsoup =  bs4.BeautifulSoup( page , "html.parser")


img_url = chsoup.select(".CurImage")[0]["src"]

img = requests.get(img_url, stream=True)
with open("test.png", "wb") as out:
    shutil.copyfileobj(img.raw, out)
del img

next = chsoup.select(".image-container > a")
#print(next)
#print(type(next[0]))
print(next[0].img)
#print(next[0]["href"])
#print(next[0]["img"])

