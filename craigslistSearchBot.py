'''
	Author: Jeffrey Trang
	Date: 06/01/2017
	Version: 1.0
	Description: Program to help automate searching user input on different sections of Craigslist.
'''

'''
	history changes
	---------------
	07/07/2017 - added printUrlsInSet function
'''

'''
	TODO Find the median price of an input object and display it on screen or
	either into a text file

	TODO: search method for mutiple items in one search

	TODO: Create a function that will take in a text file and continue appending to it in
	the form of a dictionary.
'''

#requests is a python library that lets you request information or html for a URL link i.e check if its active or if you need information
import time
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import sys

from textblob import TextBlob

import urllib, urllib2
import json

def getUserCatagory():
	catagory_to_be_searched = raw_input('Enter catagory you want to search: bikes, cars, free, sporting\n')
	catagory_to_be_searched = str(catagory_to_be_searched).lower()
	return_link = ''

	#this is a nested if to hold all the different catagory cases
	#also considered using a dictionary to implement switch case but couldnt get it to work
	if catagory_to_be_searched == 'bikes':
		return_link += "https://sandiego.craigslist.org/search/bik"
	elif catagory_to_be_searched == 'cars':
		return_link += "https://sandiego.craigslist.org/search/cto"
	elif catagory_to_be_searched == 'free':
		return_link += "https://sandiego.craigslist.org/search/zip"
	elif catagory_to_be_searched == 'sporting':
		return_link += "https://sandiego.craigslist.org/search/sga"

	return return_link

def getUserSearchItem():
	item_to_be_searched = raw_input('Enter item you want to search:\n')
	item_to_be_searched = str(item_to_be_searched).lower()
	return item_to_be_searched

'''
	input_set is the set that has the collection of all the found URLs to a searched item. This function prints out the complete set.
'''
def printUrlsInSet(input_set):
	set_to_be_printed = input_set
	print("this is a set of links: \n")
	for link in set_to_be_printed:
		print(link)

def printDictionaryItems(input_set):
	set_to_use = input_set
	for link in set_to_use:
		link_data = requests.get(link, auth=('user', 'pass'))
		link_data_parsed = BeautifulSoup(link_data.text, 'html.parser')
		title_string = link_data_parsed.find(id='titletextonly')
		#we have our title title string now ex. Leather couch free stored in title_string
		#maybe use a for loop to go through the title 
		print(title_string)

def findMedianPrice(input_set):
	for link in input_set:
		url_data = requests.get(link, auth=('user', 'pass'))
		url_data_parsed = BeautifulSoup(url_data.text, 'html.parser')
		price = url_data_parsed.findAll("span", { "class" : "price" })
		print(price)


def extractPrice(input_link):
	url_data = requests.get(input_link, auth=('user', 'pass'))
	url_data_parsed = BeautifulSoup(url_data.text, 'html.parser')
	price = url_data_parsed.findAll("span", { "class" : "price" })
	print(price)

def readCraigslist():
	url = getUserCatagory()
	item = getUserSearchItem()
	keep_searching = True
	currentRet = ''
	sent_links_set = []
	while (keep_searching):
		#request.get gets the URL link
		url_data = requests.get(url, auth=('user', 'pass'))
		#url_data_parsed is now a 'BeautifulSoup' object which represents
		#the document as a nested data structure
		url_data_parsed = BeautifulSoup(url_data.text, 'html.parser')
		for link_to_item in url_data_parsed.find_all('a'):
			if item in str(link_to_item).lower():
				# Your Account SID from twilio.com/console
				# ret = "https://edward.io/re/?u="
				ret = ''
				ret += link_to_item.get('href')
				#finalret = short_url.encode_url(ret)
				#newret = goo_shorten_url(ret)

				# account_sid = "AC5961ec0eac7ca80f65ad26e7b86a7e49"
				# Your Auth Token from twilio.com/console
				# auth_token  = "b6c1a0a74aa4af872b811e63c0c3013d"

				# client = Client(account_sid, auth_token)

				if((ret != currentRet) & (~(ret in sent_links_set))):
					
					
					# message = client.messages.create(
    	# 				to="+17609602580", 
    	# 				from_="+17606243724",
    	# 				body=ret)
    				

					currentRet = ret
					sent_links_set.append(currentRet)
					print("these are links in the current page ", ret)

		writeLinkToFile(sent_links_set)
		print("still searching...")
		time.sleep(60)

def writeLinkToFile(allLinks):
	file = open('file.txt', 'w')
	for item in allLinks:
		file.write("%s\n" % item)

def extractPriceFromTextFile(textFile):
	f = open('file.txt', 'r') 
	file = open('price.txt', 'w')
	for link in f.readlines():
		link = link.rstrip()
		url_data = requests.get(link, auth=('user', 'pass'))
		url_data_parsed = BeautifulSoup(url_data.text, 'html.parser')
		price = url_data_parsed.find("span", { "class" : "price" })
		price = price.contents
		file.write("%s\n" % (str(price).lower()))

def extractDesciptionFromTextFile(textFile):
	f = open('file.txt', 'r') 
	file = open('description.txt', 'w')
	for link in f.readlines():
		link = link.rstrip()
		url_data = requests.get(link, auth=('user', 'pass'))
		url_data_parsed = BeautifulSoup(url_data.text, 'html.parser')
		desc = url_data_parsed.find("section", { "id" : "postingbody" }).find_all(text=True, recursive=False)
		desc = str(desc).lower()
		desc = TextBlob('still runs but the engine is busted from lack of oil and needs rebuilt or the car can be used for parts.')

		print(desc.sentiment)
		sys.exit()
		file.write("%s\n" % (str(desc).lower()))
		

def testWriteMethond():
	file = open('file.txt', 'w')
	file.close()

def main():
	readCraigslist()

if __name__ == '__main__':
	main()
else:
	print('You need to run from CraigslistProgram.py')