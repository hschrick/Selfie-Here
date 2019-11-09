import tweepy
import csv
import selector
#import pandas as pd
#from PIL import Image
#import Image
import requests
from io import BytesIO
from organizer import *
import twitter_credentials



class Hashcrawler:

    def crawl(self, hashName, startTime, endTime):

        #           **********SIGN IN TO TWITTER USING KEYS FROM ANOTHER FILE **********
        auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)


        usernameList = []
        timeTweetedList = []
        messageList = []
        imageList = []
        retweetList = []
        favoriteList = []
        organizer = Organizer()


        # take an example hashtag, lets say #selfieherebostonmarathon
        # open new csv file
        csvFile = open('bm.csv', 'a')

        csvWriter = csv.writer(csvFile)




        #           **********QUERY FOR CRAWLING SPECIFIED TAGS **********
        for tweet in tweepy.Cursor(api.search, q="#selfiehere" + hashName, count=100, lang="en", since=startTime, until=endTime, include_entities=True).items():
            print(tweet.created_at, tweet.text, tweet.user.name)
            if 'media' in tweet.entities:
                for image in tweet.entities['media']:
                    print(tweet.created_at, tweet.text, tweet.user.name, image['media_url'])
                    usernameList.append(tweet.user.name)
                    timeTweetedList.append(tweet.created_at)
                    messageList.append(tweet.text)
                    imageList.append(image['media_url'])
                    retweetList.append(tweet.retweet_count)
                    favoriteList.append(tweet.favorite_count)


                    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

        #           **********SEND COLLECTED RAW DATA TO ORGANIZER **********
        organizer1 = organizer
        organizer.organize(timeTweetedList, messageList, startTime, endTime, usernameList, imageList, retweetList, favoriteList)


        return organizer1

        #send data to organizer













