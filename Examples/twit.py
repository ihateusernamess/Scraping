#!/usr/bin/env python3

import json
from watson_developer_cloud import ToneAnalyzerV3

import os
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
from time import sleep
def login():
    browser = RoboBrowser(history=True, parser='html.parser') #Load RB, keep history, supress bs4 parse warning
    browser.open('https://twitter.com/login')
    form = browser.get_form(action='https://twitter.com/sessions')#initialize form
    form['session[username_or_email]'] = 'username'
    form['session[password]'] = 'password'
    browser.submit_form(form)#submit form
    sleep(4)
    return browser
def spider(browser, twitter_url):#Goes to each tweet url and pulls bio. Also builds list of urls crawled to avoid duplicates
    users_probed = []
    for x in twitter_url:
        x = x.replace("@", "")
        if not (x in users_probed):
            browser.open('https://twitter.com/'+x)
            soup = BeautifulSoup(str(browser.select), 'lxml')
            bio = soup.find("p", {"class" : "ProfileHeaderCard-bio u-dir"}).get_text()
            print('\n\n'+x+':\t'+bio+'\n')
      
            users_probed.append(x)
def sentiment_analysis(tweets):
    tone_analyzer = ToneAnalyzerV3(
    username='',
    password='',
    version='')
    x = 0
    for t in tweets:
        print(json.dumps(tone_analyzer.tone(text=t),indent=2))
    with open("output.txt", 'a') as text_file:
        for tweet in tweets:
            text_file.write(tweet)
            x += 1
    print(str(x) + ' Tweets stored')
browser = login()#sign into twitter
soup = BeautifulSoup(str(browser.select), 'lxml')#set up bs4 object from robo browser page content

tweets = soup.findAll("div", {"class" : "content"})#build list of tweets
twitter_name = []
twitter_url = []
twitter_tweet= []
for tweet in tweets:#Passes each tweet in the list and stores user id, user url, and tweet content in seperate lists
    twitter_name.append(tweet.find("strong", {"class" : "fullname show-popup-with-id "}).get_text())
    twitter_url.append(tweet.find('span', {'class' : "username u-dir"}).get_text())
    twitter_tweet.append(tweet.find('div', {'class': "js-tweet-text-container"}).get_text())
for name, url, content in zip(twitter_name,twitter_url,twitter_tweet):#Goes through lists of tweet content scraped
    print('Alias: '+name+'\t'+url+'\nTweet:\n'+content)
spider(browser, twitter_url)
sentiment_analysis(twitter_tweet)



