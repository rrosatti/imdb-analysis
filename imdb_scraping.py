from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

coming_soon_url = 'http://www.imdb.com/movies-coming-soon/'
movie_url = 'http://www.imdb.com'

def get_new_movies_coming_soon():
	# get current date and the date for the next two months
	now = datetime.now()
	next_month = now + relativedelta(months=+1)
	next_month_2 = next_month + relativedelta(months=+1)
	# format dates to Y-m
	now = now.strftime('%Y-%m')
	next_month = next_month.strftime('%Y-%m')
	next_month_2 = next_month_2.strftime('%Y-%m')

	soup_coming_soon = BeautifulSoup(requests.get(coming_soon_url+next_month).text, 'html5lib')
	# the movies are inside tables
	movies = soup_coming_soon.find_all('table', class_='nm-title-overview-widget-layout')

	# get a list of the movies url
	movies_url_list = []
	for movie in movies:
		movie_href = movie.find_all('h4')[0].find('a')
		movie_href = movie_href.get('href')
		movies_url_list.append(movie_url+movie_href)

	for m_url in movies_url_list:
		print(m_url)
		soup_movie_page = BeautifulSoup(requests.get(m_url).text, 'html5lib')
		print(soup_movie_page)
		break	
