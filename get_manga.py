from pprint import pprint
import shutil

import bs4
import requests

BASE_URL = "http://mangalife.us"

def get_first_chapter_location(name):
  listing_url = BASE_URL + "/manga/" +  "-".join(name.split())
  listing_html = requests.get(listing_url).text
  listing_soup = bs4.BeautifulSoup( listing_html , "html.parser")
  return listing_soup.select(".list-group-item")[-1]["href"]

def download_image(img_url, name):
  img = requests.get(img_url, stream=True)
  with open("tmp/{}.png".format(name), "wb") as out:
    shutil.copyfileobj(img.raw, out)
  del img

def get_manga(name):
  next_page_html = requests.get( BASE_URL + get_first_chapter_location(name)).text
  page_num = 1

  while(True):
    pg_soup =  bs4.BeautifulSoup( next_page_html, "html.parser")
    image_container = pg_soup.select(".image-container > a")[0]
    download_image(image_container.img["src"], page_num)
    page_num+=1
    next_page_html = requests.get( BASE_URL + image_container["href"]).text

  # pg_soup =  bs4.BeautifulSoup( ch1pg1_html , "html.parser")
# 
  # page_num = 1
  # image_container = pg_soup.select(".image-container > a")[0]
  # download_image(image_container.img["src"], page_num)
  # page_num+=1
# 
  # next_page_html = requests.get( BASE_URL + image_container["href"]).text
  # pg_soup =  bs4.BeautifulSoup( next_page_html, "html.parser")
  # image_container = pg_soup.select(".image-container > a")[0]
  # download_image(image_container.img["src"], page_num)
  # page_num+=1



if __name__ == "__main__":
  get_manga("boku no hero academia")
