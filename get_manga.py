import os
from pprint import pprint
import shutil

import bs4
import img2pdf
import requests


def convert_imgs_to_pdf(pdf_name, target_dir, dest_dir):
    num_of_pages= len([name for name in os.listdir(target_dir)])
    files = [ "{}/{}".format(target_dir, i) for i in range(1,num_of_pages)]
    pdf_bytes = img2pdf.convert(files)
    file = open("{}/{}.pdf".format(dest_dir, pdf_name), "wb")
    file.write(pdf_bytes)


def get_chapter_list(url):
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, "html_parser")
    # chapters are retrieved in reversed order, so we reverse it again
    return list(reversed([chapter["href"] for chapter in soup.select(".list-group-item")]))


def download_image(img_url, source_dir, name):
    img = requests.get(img_url, stream=True)
    with open("{}/{}".format(source_dir, name), "wb") as out:
        shutil.copyfileobj(img.raw, out)


def download_page_range_by_url(manga_name, base_url, start_url, end_url, chapter_num):
    tmp_chapter_dir = "temp_chapter_dir"
    try:
        os.mkdir(manga_name)
    except FileExistsError:
        pass
    try:
        os.mkdir(tmp_chapter_dir)
    except FileExistsError:
        shutil.rmtree(tmp_chapter_dir)
        os.mkdir(tmp_chapter_dir)

    end_page_url = base_url + end_url
    next_page_url = base_url + start_url
    page_num = 1
    while(next_page_url != end_page_url):
        next_page_html = requests.get(next_page_url).text
        pg_soup =  bs4.BeautifulSoup( next_page_html, "html.parser")
        image_container = pg_soup.select(".image-container > a")[0]
        download_image(image_container.img["src"], tmp_chapter_dir, page_num)
        page_num+=1
        next_page_url = base_url + image_container["href"]
    chapter_name = f"CH{chapter_num}"
    convert_imgs_to_pdf(chapter_name, tmp_chapter_dir, manga_name)
    shutil.rmtree(tmp_chapter_dir)


def download_chapters(manga_name, url, start_chapter, end_chapter):
    chapter_listing = get_chapter_list(url)
    chapter_num = start_chapter
    while(chapter_num != end_chapter+1):
        first_page_url = chapter_listing[chapter_num - 1]
        last_page_url = chapter_listing[chapter_num]
        # TODO: do not harcode first argument if expanded into other urls
        download_page_range_by_url(manga_name,
                                   'http://mangalife.us',
                                   first_page_url,
                                   last_page_url,
                                   chapter_num)
        chapter_num += 1


if __name__ == "__main__":
    download_chapters("boku_no_hero", "http://mangalife.us/manga/Boku-No-Hero-Academia", 1, 10)

