# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request as req
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import sys
import json
from urllib.error import HTTPError
import numpy as np

title_list = []
combine_list2 = [] #contains df first four columns

def writeToExcel(data):
	df = pd.DataFrame(data, columns = ['Title', 'Year', 'Genre', 'IMDB rating'])
	df['tomato_meter'] = tomato_meter
	df['audience_rotten_tomatoes'] = audi_score
	df.to_excel("output.xlsx")
	print(".... written to excel")

#gets data response for the request
def getResponse(reqURL):
	print("in getResponse() ")
	response = req.urlopen(reqURL) #opens url
	data = response.read() #reads the whole page source 
	print("printing data")
	#print(type(data))
	return data


def getTopThrillers(url):
	print(url)
	print("in getTopThrillers() ")
	data = getResponse(url)
	soup = BeautifulSoup(data, 'html.parser')
	#print(soup.prettify()) #displays page source info in pretty form


	movie_name_list = []
	ratings_list = []
	
	for show in soup.find_all('div', {'class' :'lister-item-content'}):
		#print(show)
		if "Filming" not in str(show):
			for show in show.find_all('div', {'class' :'inline-block ratings-imdb-rating'}):
				ratings_list.append(show.text.strip().split("\n"))

		else:
			print("hereeeeeeeeeee")
			ratings_list.append("-")

	
	for show in soup.find_all('h3', {'class' :'lister-item-header'}):
		movie_name_list.append(show.text.strip().split("\n")[1])
		title_list.append(show.text.strip().split("\n")[1])

	rows = [show.text.strip().split("\n")[0] for show in soup.find_all('h3', {'class' :'lister-item-header'})]
	year_list = [show.text.strip().split("\n")[2] for show in soup.find_all('h3', {'class' :'lister-item-header'})]
	genre_list = [show.text.strip().split("\n") for show in soup.find_all('span', {'class' :'genre'})]
	

	# print(movie_name_list)
	combine_list1 = []

	temp = ""
	
	for row, m, y, g, r in zip(rows, movie_name_list, year_list, genre_list, ratings_list):

	  	combine_list1.extend((row.strip(), m.strip(' '), y.strip(' '), str(g).strip('[]').replace("'",""), str(r).strip('[]').replace("'","") ))
	  	combine_list2.append(combine_list1)
	  	combine_list1 = []

	for ele in combine_list2:
	    print(ele)
	# writeToExcel(combine_list2)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def getResponse_rotten_tomato(url, title):
	print("in getResponse_rotten_tomato")
	
	data = ""
	if is_ascii(title) == False: return "-"
	try:
		#print("in try loop")
		final_url = url + "tv/" + title
		print(final_url)
		response_tv = req.urlopen(final_url) #opens url
		data = response_tv.read()
		#print(type(data))
		return data
		

	except HTTPError as e:
		# print("here")
		# print(type(e.code))
		if e.code == 404:

		    #print("here2")
		    try:
		    	final_url = url+ "m/" + title
		    	print(final_url)
		    	response_m = req.urlopen(final_url) #opens url
		    	data = response_m.read()

		    	if len(data) != 0:
		    	    return data
		    	else:
		    		return "-"
		    except HTTPError as e:
		    	return "-"

		    
tomato_meter = []
audi_score = []
def getRottenTomatoesRating(data):

	print("in getRottenTomatoesRating() ")
	soup = BeautifulSoup(data, 'html.parser')
	rating = [percent.text.strip() for percent in soup.find_all('span', {'class' : 'mop-ratings-wrap__percentage'})]
	print(rating)

	if len(rating) == 2:
		tomato_meter.append(rating[0])
		audi_score.append(rating[1])

	elif len(rating) == 1:
		tomato_meter.append("-")
		audi_score.append(rating[0])
	else:
		tomato_meter.append("-")
		audi_score.append("-")


	
def main():
	page = [i for i in range(1,50,50)]
	print(page)
	for pg in page :
		base_url = "https://www.imdb.com/search/title/?genres=thriller&start="+ str(pg) + "&ref_=adv_nxt"
		getTopThrillers(base_url)

	
	#title_list = ['Ozark', 'Élite', 'La Casa de Papel', 'El hoyo', 'The Walking Dead', 'Contagion', 'Bad Boys for Life', 'Killing Eve', 'The Invisible Man', 'Underwater']
	#base_url = "https://www.rottentomatoes.com/search?search="
	
	# combine_list2 = [['Ozark', '(2017– )', 'Crime, Drama, Thriller', '8.4'], ['La Casa de Papel', '(2017– )', 'Action, Crime, Mystery', '8.5'], ['El hoyo', '(2019)', 'Horror, Sci-Fi, Thriller', '7.0'], ['The Walking Dead', '(2010– )', 'Drama, Horror, Thriller', '8.2'], ['Contagion', '(2011)', 'Action, Drama, Thriller', '6.7'], ['Bad Boys for Life', '(2020)', 'Action, Comedy, Crime', '6.8'], ['Killing Eve', '(2018– )', 'Action, Adventure, Drama', '8.3'], ['The Invisible Man', '(2020)', 'Horror, Mystery, Sci-Fi', '7.2'], ['Underwater', '(2020)', 'Action, Drama, Horror', '5.9'], ['Knives Out', '(2019)', 'Comedy, Crime, Drama', '8.0'], ['Gisaengchung', '(2019)', 'Comedy, Drama, Thriller', '8.6'], ['Homeland', '(2011–2020)', 'Crime, Drama, Mystery', '8.3'], ['Breaking Bad', '(2008–2013)', 'Crime, Drama, Thriller', '9.5'], ['The Hunt', '(II) (2020)', 'Action, Horror, Thriller', '6.4'], ['Supernatural', '(2005– )', 'Drama, Fantasy, Horror', '8.4'], ['The Blacklist', '(2013– )', 'Crime, Drama, Mystery', '8.0'], ['Élite', '(2018– )', 'Crime, Drama, Thriller', '7.6'], ['Stranger Things', '(2016– )', 'Drama, Fantasy, Horror', '8.8'], ['Altered Carbon', '(2018– )', 'Action, Drama, Sci-Fi', '8.1'], ['Black Mirror', '(2011– )', 'Drama, Sci-Fi, Thriller', '8.8'], ['The Outsider', '(2020– )', 'Crime, Drama, Mystery', '8.0'], ['Spenser Confidential', '(2020)', 'Action, Comedy, Crime', '6.2'], ['Uncut Gems', '(2019)', 'Crime, Drama, Thriller', '7.5'], ['Criminal Minds', '(2005–2020)', 'Crime, Drama, Mystery', '8.1'], ['Devs', '(2020– )', 'Drama, Mystery, Sci-Fi', '7.9'], ['Joker', '(2019)', 'Crime, Drama, Thriller', '8.5'], ['Asur: Welcome to Your Dark Side', '(2020– )', 'Crime, Drama, Thriller', '8.6'], ['Law & Order: Special Victims Unit', '(1999– )', 'Crime, Drama, Mystery', '8.0'], ['Locke & Key', '(2020– )', 'Drama, Fantasy, Horror', '7.4'], ['Midsommar', '(2019)', 'Drama, Horror, Mystery', '7.1'], ['Fargo', '(2014– )', 'Crime, Drama, Thriller', '8.9'], ['The Wire', '(2002–2008)', 'Crime, Drama, Thriller', '9.3'], ['The Sinner', '(2017– )', 'Crime, Drama, Mystery', '8.0'], ['American Horror Story', '(2011– )', 'Drama, Horror, Thriller', '8.1'], ['Dark', '(2017– )', 'Crime, Drama, Mystery', '8.7'], ['You', '(2018– )', 'Crime, Drama, Romance', '7.8'], ['NCIS: Naval Criminal Investigative Service', '(2003– )', 'Action, Crime, Drama', '7.8'], ["The Handmaid's Tale", '(2017– )', 'Drama, Sci-Fi, Thriller', '8.5'], ['The Stranger', '(I) (2020– )', 'Mystery, Thriller', '7.4'], ['Toy Boy', '(2019)', 'Crime, Drama, Thriller', '6.5'], ['Hogar', '(2020)', 'Drama, Thriller', '6.4'], ['Defending Jacob', '(2020– )', 'Mystery, Thriller', '8.1'], ['Chicago P.D.', '(2014– )', 'Action, Crime, Drama', '8.1'], ['How to Get Away with Murder', '(2014– )', 'Crime, Drama, Mystery', '9.4'], ['Chernobyl', '(2019)', 'Drama, History, Thriller', '8.3'], ['Prison Break', '(2005–2017)', 'Action, Crime, Drama', '9.0'], ['True Detective', '(2014– )', 'Crime, Drama, Mystery', '8.3'], ['Kingdom', '(2019– )', 'Action, Drama, Horror', '9.1'], ['Sherlock', '(2010– )', 'Crime, Drama, Mystery', '8.8']]
	
	# base_url = "https://www.rottentomatoes.com/"

	# titles = np.array(combine_list2)

	# for title in titles[:,0]:
	# 	print()
	# 	print(title)
	# 	#title = str(title.replace(" ","_").encode('utf-8'))
	# 	title = title.replace(" ","_")
		
	# 	ret = getResponse_rotten_tomato(base_url,title)
	# 	#print(type(ret))
		
		
	# 	if not isinstance(ret,type(None)): 	
	# 		getRottenTomatoesRating(ret)

	# 	else: 
	# 		tomato_meter.append("-")
	# 		audi_score.append("-")


	# # print(tomato_meter)
	# # print(audi_score)
	# # print(combine_list2)

	# # tomato_meter = ['81%', '90%', '-', '81%', '-', '77%', '87%', '50%', '-', '97%', '-', '85%', '96%', '-', '93%', '91%', '-', '93%', '76%', '83%', '82%', '39%', '92%', '-', '82%', '-', '-', '-', '-', '83%', '96%', '94%', '95%', '-', '94%', '90%', '-', '-', '-', '-', '-', '-', '-', '90%', '96%', '60%', '78%', '80%', '78%', '89%']
	# # audi_score = ['92%', '84%', '-', '78%', '-', '96%', '89%', '50%', '15%', '92%', '-', '86%', '98%', '100%', '86%', '89%', '-', '91%', '63%', '81%', '85%', '57%', '52%', '87%', '68%', '33%', '-', '-', '-', '63%', '93%', '97%', '75%', '76%', '94%', '81%', '-', '-', '83%', '40%', '100%', '-', '-', '86%', '98%', '77%', '78%', '89%', '83%', '94%']
	# print(len(tomato_meter))
	# print(len(audi_score))
	print(len(combine_list2))
	# writeToExcel(combine_list2)


if __name__ == "__main__":
	main()