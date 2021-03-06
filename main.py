import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests


# First dataset for testing
"""
sites = [
    "https://www.snopes.com/fact-check/hillary-clinton-smash-phone-hammer/",
    "https://africacheck.org/reports/eskom-and-the-viral-infographic-do-the-numbers-add-up/",
    "http://checkyourfact.com/2018/07/09/fact-check-nfl-ratings-20-percent/",
    "https://www.factcheck.org/2018/07/trumps-false-claims-at-nato/",
    "https://theferret.scot/scotland-oil-abu-dhabi-dubai/",
    "https://fullfact.org/europe/uk-one-biggest-contributors-eu-budget/?utm_source=homepage&utm_medium=main_story",
    "https://hoax-alert.leadstories.com/3469573-fake-news-florida-babysitter-tied-crying-one-month-old-baby-to-ceiling-fan-for-26-hours.html",
    "https://pesacheck.org/have-58-of-ugandas-roads-been-built-using-only-government-money-e2156f2aa41a",
    "http://www.politifact.com/personalities/sean-hannity/",
    "https://theconversation.com/factcheck-is-australias-population-the-highest-growing-in-the-world-96523",
    "https://www.washingtonpost.com/news/fact-checker/wp/2018/07/18/phil-bredesens-claim-that-tennessees-meth-problem-was-cut-in-half/?utm_term=.f3688d506f6c",
]
language = 'english'
"""

"""
# Complement in english
sites = [
    "https://www.rappler.com/newsbreak/fact-check/210221-naga-not-top-5-city-crime-volume-philippines",
    "https://www.snopes.com/fact-check/john-mccain-last-words-trump/",
    "http://verafiles.org/articles/vera-files-fact-check-duterte-wrong-saying-mindanao-not-hit",
    "https://www.factcheckni.org/facts/100000-adults-northern-ireland-no-home/",
    "http://www.abc.net.au/news/2018-08-23/fact-check-fraser-anning-university-places-international-student/10147364",
]
language = 'english'
"""

# Portuguese news

sites = [
    "https://piaui.folha.uol.com.br/lupa/2018/08/08/presidenciaveis-seguranca-globonews/",
    "https://aosfatos.org/noticias/alckmin-cita-dados-errados-sobre-numero-de-penitenciarias-e-consumo-de-drogas-na-globonews/",
    "https://apublica.org/2018/07/truco-paulo-rabello-acerta-gasto-em-educacao-e-erra-mortes-de-negros/",
    "https://g1.globo.com/e-ou-nao-e/noticia/2018/07/23/placa-mostra-que-a-igreja-universal-explora-estacionamento-da-lagoa-no-rio-nao-e-verdade.ghtml",
    "http://www.e-farsas.com/manuela-davila-aparece-em-video-dancando-funk-na-rua-sera-verdade.html",
]
language = 'portuguese'


ignore_html_tags = ['script']
text_tags = ['p', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'li', 'b', 'i', 'u', 'title', 'em']


def treat_text(text):
    return text.replace('\n', '').replace('\t', '').strip()


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
    if element is None:
        return
    features['tag'] = element.name
    features['attrs'] = element.attrs
    #features['attrs'] = treat_text(';'.join(element.attrs))
    #features['attrs_values'] = treat_text(';'.join([' '.join(element.attrs[k]) for k in element.attrs]))
    features['url'] = site
    features['level'] = level
    features['label'] = 'None'
    features['language'] = language
    if element.name in text_tags:
        features['text'] = treat_text(element.text)
    else:
        features['text'] = 'NOT TEXT'

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
    for url in sites:
        data=[]
        print('url:', url)
        html = get_url(url)
        extract_features(html, data, url)
        pdf=pd.DataFrame(data)
        pdf.to_csv("features"+str(sites.index(url))+".csv", encoding="utf8")
