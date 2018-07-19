import pandas as pd

import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import datetime
import dateparser
import copy
import Claim as claim_obj
import requests
from dateparser.search import search_dates
	


sites=[ "https://www.snopes.com/fact-check/hillary-clinton-smash-phone-hammer/",
]


def get_url(url):
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

	try:
		page = requests.get(url, headers=headers, timeout=5)
		soup = BeautifulSoup(page.text,"lxml")
		return soup.prettify()
	except:
		return none


#to do
def extract_features(html):

	return none




if __name__ == "__main__":
	data=[]
    for url in sites:
    	html = get_url(url)
    	features = {}
    	feature  = extract_features(html)
    	data.append(featuers)

    pdf=pd.DataFrame(data)
    pdf.to_csv("features.csv",encoding="utf8")


