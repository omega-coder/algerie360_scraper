#!/usr/bin/ env python

import re
import sys
from bs4 import BeautifulSoup
import requests
import json


session = requests.Session()
articles = []

def parse_article(link):
    r = session.get(link)
    if r.status_code != 200:
        print("Can't connect")
    data_html = r.text
    soup = BeautifulSoup(data_html, 'lxml')
    title = soup.select("#titrepost")[0].h1.getText()
    content_paragraphs = soup.find("div", class_="postwhite").select("p")
    content = ""
    for p in content_paragraphs:
        content += p.getText()

    author = "algerie360"
    date_elem = soup.find("div", class_="datearti")
    if date_elem is None:
        print("WTF")
        print(title)
    date = date_elem.getText().lstrip()
    return date, author, content, title

def parse_page_articles(link, page):
    r = session.get(link+"/page/"+str(page))
    if r.status_code == 200:
        data = r.text
        article_elements = BeautifulSoup(r.text, 'lxml').find_all("div", class_="blocactucat")
    else:
        print("error")

    for elem in article_elements:
        art = {"title": "", "date": "", "author": "", "link": "", "source": "", "content": ""}
        a = BeautifulSoup(elem.h2.encode(), 'lxml')
        art["link"] = a.a["href"]
        date, author, content, title = parse_article(art["link"])
        art["date"] = date
        art["author"] = author
        art["content"] = content
        art["source"] = "algerie360"
        art["title"] = title
        articles.append(art)

    print("Parsed {} articles till now ".format(len(articles)))

def main(cat_url):
    for page in range(1, 2):
        parse_page_articles(cat_url, page)
    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False)

if __name__ == "__main__":
    category_url = "https://www.algerie360.com/category/economie/"
    main(category_url)
