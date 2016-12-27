from bs4 import BeautifulSoup
import requests, re
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import imdb_util as iutil

coming_soon_url = 'http://www.imdb.com/movies-coming-soon/'
imdb_url = 'http://www.imdb.com'

def get_new_movies_coming_soon():
	# get current date and the date for the next two months
	now = datetime.now()
	next_month = now + relativedelta(months=+1)
	#next_month_2 = next_month + relativedelta(months=+1)
	# format dates to Y-m
	now = now.strftime('%Y-%m')
	next_month = next_month.strftime('%Y-%m')
	#next_month_2 = next_month_2.strftime('%Y-%m')

	# check if the file already exists
	if iutil.file_exists(next_month+'.pickle'):
		detailed_movies_list = iutil.get_pickle(next_month+'.pickle')
	else:
		soup_coming_soon = BeautifulSoup(requests.get(coming_soon_url+next_month).text, 'html5lib')
		# the movies are inside tables
		movies = soup_coming_soon.find_all('table', class_='nm-title-overview-widget-layout')

		# get a list of movies url
		movies_url_list = []
		for movie in movies:
			movie_href = movie.find_all('h4')[0].find('a')
			movie_href = movie_href.get('href')
			movies_url_list.append(movie_href)

		detailed_movies_list = get_movie_info(movies_url_list, imdb_url)
		print(detailed_movies_list)
		iutil.save_pickle(detailed_movies_list, next_month+'.pickle')	

	# convert from list of dicts to DataFrame	
	df = pd.DataFrame(detailed_movies_list)
	df = df[['movie_title', 'movie_year', 'movie_facebook_likes', 'director_name', 'director_facebook_likes', 
				'actor_1_name', 'actor_1_facebook_likes', 'actor_2_name', 'actor_2_facebook_likes',
				'actor_3_name', 'actor_3_facebook_likes', 'cast_total_facebook_likes', 'plot_keywords']]
	#print(df)
	return df

def get_movie_info(url_list, imdb_url):
	movies_info_list = []
	for m_url in url_list:
		movie_detail = {}
		soup_movie_page = BeautifulSoup(requests.get(imdb_url+m_url).text, 'html5lib')
		
		# movie title and year Ex: Underworld: Blood Wars (2016)
		movie_detail['movie_title'], movie_detail['movie_year'] = get_movie_title_and_year(soup_movie_page)
		print(movie_detail['movie_title'])
		
		# get director name and link
		movie_detail['director_name'], movie_detail['director_link'] = get_director_name_and_link(soup_movie_page)

		# get actors name and link
		actors_info = get_actors_name_and_link(soup_movie_page)
		movie_detail.update(actors_info)

		# get plot keywords
		movie_detail['plot_keywords'] = get_plot_keywords(soup_movie_page)
		
		# movie facebook likes
		movie_detail['movie_facebook_likes'] = get_movie_facebook_likes(m_url.split('/')[2])

		# get people facebook likes
		movie_detail['director_facebook_likes'] = get_people_facebook_likes(movie_detail['director_link'])
		movie_detail['actor_1_facebook_likes'] = get_people_facebook_likes(movie_detail['actor_1_link'])
		movie_detail['actor_2_facebook_likes'] = get_people_facebook_likes(movie_detail['actor_2_link'])
		movie_detail['actor_3_facebook_likes'] = get_people_facebook_likes(movie_detail['actor_3_link'])

		# get cast total facebook likes
		movie_detail['cast_total_facebook_likes'] = (movie_detail['director_facebook_likes'] + movie_detail['actor_1_facebook_likes']
			+ movie_detail['actor_2_facebook_likes'] + movie_detail['actor_3_facebook_likes'])		

		movies_info_list.append(movie_detail)
		#print(movie_detail)

	return movies_info_list	

def get_movie_title(soup):
	return soup.find('meta', property='og:title')['content']

def get_movie_year(mtitle): 
	return mtitle[mtitle.find('(')+1:mtitle.find(')')]

def get_movie_title_and_year(soup):
	mtitle = soup.find('meta', property='og:title')['content']
	myear = mtitle[mtitle.find('(')+1:mtitle.find(')')]
	mtitle = re.sub(r'\([^)]*\)', '', mtitle).rstrip()
	return mtitle, myear

def get_director_name_and_link(soup):
	director = soup.find('div', class_='credit_summary_item').find_all('a')[0]
	dname = director.text
	dlink = director.get('href')
	return dname, dlink		

def get_actors_name_and_link(soup):
	actors_info = {}
	try:
		for i, m in enumerate(soup.find_all('div', class_='credit_summary_item')[2].find_all('a')[:-1]):
			actors_info['actor_'+str(i+1)+'_name'] = m.text
			actors_info['actor_'+str(i+1)+'_link'] = m.get('href')
		if len(actors_info) == 3:
			return actors_info
		else:
			for i in range(len(actors_info), 3):
				actors_info['actor_'+str(i+1)+'_name'] = None
				actors_info['actor_'+str(i+1)+'_link'] = None
			return actors_info

	except Exception as e:
		print(str(e))
		for i in range(len(actors_info), 3):
			actors_info['actor_'+str(i+1)+'_name'] = None
			actors_info['actor_'+str(i+1)+'_link'] = None
		return actors_info
		

def get_plot_keywords(soup):
	keywords = []
	try:
		for k in soup.find('div', class_='see-more inline canwrap', itemprop='keywords').find_all('a')[:-1]:
			keywords.append(k.text.lstrip())
		return '|'.join(keywords)
	except Exception as e:
		print(str(e))
		return None

def get_movie_facebook_likes(movie_id):
	url = "https://www.facebook.com/widgets/like.php?width=280&show_faces=1&layout=standard&href=http://www.imdb.com/title/{}/&colorscheme=light".format(movie_id)
	try:
		soup = BeautifulSoup(requests.get(url, headers={"Accept-Language": "en-US,en;q=0.5"}).text, 'html5lib')
		sentence = soup.find_all(id='u_0_2')[0].span.string  # 16K people like this
		num_likes = sentence.split(' ')[0]
		if 'K' in num_likes:
			num_likes = num_likes[:-1]
			num_likes = float(num_likes)*1000
		return float(num_likes)
	except Exception as e:
		print(str(e))
		return 0

def get_people_facebook_likes(people_id):
	if people_id is not None:
		people_id = people_id.split('/')[2].split('?')[0]
	else:
		return 0

	url = "https://www.facebook.com/widgets/like.php?width=280&show_faces=1&layout=standard&href=http://www.imdb.com/name/{}/&colorscheme=light".format(people_id)
	try:
		soup = BeautifulSoup(requests.get(url, headers={"Accept-Language": "en-US,en;q=0.5"}).text, 'html5lib')
		sentence = soup.find_all(id='u_0_2')[0].span.string  # 16K people like this
		num_likes = sentence.split(' ')[0]
		if 'K' in num_likes:
			num_likes = num_likes[:-1]
			num_likes = float(num_likes)*1000
		return float(num_likes)
	except Exception as e:
		print(str(e))
		return 0
