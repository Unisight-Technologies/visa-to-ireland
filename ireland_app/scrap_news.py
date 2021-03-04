import urllib.request
import urllib.error
import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests



# Create all_h1_tags as empty list
def get_title(soup):
	titles = []
	# Set all_h1_tags to all h1 tags of the soup
	for div in soup.findAll('h4',
								attrs = {'class':'title'}):
			    titles.append(div.text.strip())
	return titles


def get_date(soup):
	dates = []
	for div in soup.findAll('h3'):
	            dates.append(div.text.strip())
	return dates


def get_description(soup):
	descriptions = []
	for div in soup.findAll('p',
	                           attrs = {'class':'excerpt'}):
			   descriptions.append(div.text.strip())
	return descriptions


def get_url(soup):
	links = []

	for div in soup.findAll('h4',
								attrs = {'class':'title'}):
		links.append(div.find('a')['href'])
	return links




class Scrapper():
	def __init__(self):
		req = Request('https://www.thejournal.ie/immigration/news/', headers={'User-Agent': 'Mozilla/5.0'})
		URL = "https://www.thejournal.ie/immigration/news/"
		html = urllib.request.urlopen(req).read()
		soup = BeautifulSoup(html, 'html.parser')

		self.titles = get_title(soup)
		self.dates = get_date(soup)
		self.descriptions = get_description(soup)
		self.urls = get_url(soup)
