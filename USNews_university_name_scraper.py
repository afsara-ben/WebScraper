# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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
	df = pd.DataFrame(data, columns = ['Name', 'Rank', 'location' ,'Score'])
	# df['tomato_meter'] = tomato_meter
	# df['audience_rotten_tomatoes'] = audi_score
	df.to_excel("output_uni_names.xlsx")
	print(".... written to excel")

#gets data response for the request
def getResponse(reqURL):
	print("in getResponse() ")

	chrome_options = Options()
	chrome_options.add_argument("--disable-extensions")
	
	driver = webdriver.Chrome(options=chrome_options, executable_path = '/home/afsara-ben/Desktop/dl_movie_name/WebScraper/chromedriver')
	driver.implicitly_wait(30)

	driver.get(reqURL)
	scroll(driver,5)

	# response = req.urlopen(reqURL) #opens url
	# data = response.read() #reads the whole page source 
	# print("printing data")
	# #print(type(data))

	
	return driver.page_source


def scroll(driver, timeout):
	scroll_pause_time = timeout
	
	#get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		#scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		#wait for page to load
		time.sleep(scroll_pause_time)

		#calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break

		last_height = new_height

def getUniNames(url):
	print(url)
	print("in getUniNames() ")
	data = getResponse(url)
	soup = BeautifulSoup(data, 'lxml')
	#soup = BeautifulSoup(data, 'html.parser')
	print("printing soup")
	#print(soup.prettify()) #displays page source info in pretty form


	rank_list = []
	uni_name_list = []
	location = []
	peer_score = []
	score = []
	
	for names in soup.find_all('h3', {'class' :'Heading-bocdeh-1 iqkCSQ Heading__HeadingStyled-bocdeh-0-h3 dtIFQE'}):
		
		for name in names.find_all('a'):
			uni_name_list.append(name.text.strip().split("\n"))

	
	for names in soup.find_all('strong', {'class' :'NameRank__RankPosition-s4melbd-0 Wtokh Strong-s144f3me-0 cRVRij'}):
		
		rank_list.append(names.text.strip().split("\n"))
	# #print(rank_list)

	rank_plus_loc = [loc.text.strip().split("\n") for loc in soup.find_all('p', {'class' :'Paragraph-s10q84gy-0 bgyixv'})]
	
	#extract only the locations
	for i in range(len(rank_plus_loc)):
		if i % 2 == 0:
			location.append(rank_plus_loc[i])

	

	for score in soup.find_all('span', {'class' :'Span-aabx0k-0 RNL'}):
		peer_score.append(score.text.strip().split("\n")) 	

	for s in peer_score[::2]:
		score.append(s)


	# score.pop(0)
	# score.pop(0)
	print(score)
	combine_list1 = []

	print(len(uni_name_list))
	print(len(rank_list))
	print(len(location))
	print(len(peer_score))

	
	
	for Name, rank, loc, score in zip(uni_name_list, rank_list, location, peer_score):
		
		#print(str(Name) + " - " + str(rank) + " - "+ str(loc))
		combine_list1.extend((str(Name).strip('[]').replace("'",""), str(rank).strip('[]').replace("#","").replace("'",""),str(loc).strip('[]').replace("#","").replace("'",""), str(score).strip('[]').replace("'","")))
		combine_list2.append(combine_list1)
		combine_list1 = []

	for ele in combine_list2:
	    print(ele)
	writeToExcel(combine_list2)


	
def main():
	
	base_url = "https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings"
	getUniNames(base_url)



if __name__ == "__main__":
	main()