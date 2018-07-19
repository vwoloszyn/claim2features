import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
    

sites = [
    "https://www.snopes.com/fact-check/hillary-clinton-smash-phone-hammer/",
]

ignore_html_tags = ['script']


def get_url(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(page.text,"lxml")
        soup.prettify()
        return soup
    except:
        return None


def walk_html(element, data, site, level):
    features = {}
    features['tag'] = element.name
    features['url'] = site
    features['level'] = level
    features['label'] = 'None'
    if len(list(element))==0:
        features['text'] = element.text
    else:
        features['text'] = 'NOT LEAF'

    data.append(features)
    for e_child in element:
        if (type(e_child) == bs4.element.NavigableString or 
            type(e_child) == bs4.element.Comment or 
            type(e_child) == bs4.element.Doctype or 
            type(e_child) == str or
            e_child.name in ignore_html_tags):
            continue
        walk_html(e_child, data, site, level+1)

def extract_features(html, data, site):
    walk_html(html, data, site, 0)


if __name__ == "__main__":
    data=[]
    for url in sites:
        html = get_url(url)
        extract_features(html, data, url)

    pdf=pd.DataFrame(data)
    pdf.to_csv("features.csv", encoding="utf8")
