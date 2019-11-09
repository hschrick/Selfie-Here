import selector
import hashcrawler
import interface
from Analyzer import *
from colorama import Fore, Back, Style

class Organizer:

    def __init__(self):
        self.tweetNames = []
        self.messages = []
        self.timesAttended = []
        self.tweetImages = []
        self.retweetList = []
        self.favoriteList = []
        self.userSentiment = []

    def organize(self, tweetTime, tweetMessage, tweetAttendanceStart, tweetAttendanceEnd, tweetName, timage, rtList, fList):

        self.tweetNames = tweetName

        self.messages = tweetMessage

        self.timesAttended = tweetTime
        self.take_attendance(self.timesAttended, tweetAttendanceStart, tweetAttendanceEnd)

        self.tweetImages = timage

        self.retweetList = rtList

        self.favoriteList = fList

        self.find_popular_tweets()

        self.message_clipper()

    # **********combines retweets and favorites of each user and finds the most popular**********
    def find_popular_tweets(self):

        rtlist = self.retweetList
        fvlist = self.favoriteList

        users = rtlist

        # **********Combine rts and likes for each user**********
        for i in users:
            users[i] += fvlist[i]

        #filter out the most popular tweet
        max = 0

        for usermax in users:

            if (usermax > max):
                max = usermax

        print("The most popular tweet is: " + str(max))


    """""
    compares times attended with expected attendance and colors accordingly.
    """""
    def take_attendance(self, tAttended, tweetAttendanceStart, tweetAttendanceEnd):

        #clean up custom start time
        tweetAttendanceStart = str(tweetAttendanceStart)
        newStart = tweetAttendanceStart.strip()
        newStart = newStart.replace("-", "")
        newStart = newStart.replace(":", "")

        #clean up custom end time
        newEnd = tweetAttendanceEnd.replace(" ", "")
        newEnd = newEnd.replace("-", "")
        newEnd = newEnd.replace(":", "")

        # clean up each attendents time
        tAttended = str(tAttended)
        newtime = tAttended.replace(" ", "")
        newtime = newtime.replace("-", "")
        newtime = newtime.replace(":", "")

        #build a comparison to test for lateness



        #currently counts a day after start as late just for testing.
        late = str(int(newStart) + 1)




        #compare user time with start time and end time
        if (newtime >= late and newtime <= newEnd):
            return 'Time: [color=#8B0000]{}[/color]\n'.format(tAttended)
        if(newtime >= newStart and newtime <= newEnd):
            return 'Time: [color=#7CFC00]{}[/color]\n'.format(tAttended)

    #*****Sentiment Analyzer*****

    #*****Cleans up tweets into message blocks*****
    def message_clipper(self):

        cleanMessages = []

        for i in self.messages:
            dirtyMessage = i.split()
            dirtyMessage.pop(0)
            del dirtyMessage[-1]
            cleanMessages.append(dirtyMessage)

        self.detect_sentiment(cleanMessages)

        print("message is " + str(cleanMessages[0]))

    #*****Ajusts and sets sentiment ranks for each user*****
    def detect_sentiment(self, messages):

        finalSentiment = 0

        previousWord = None

        prevExtension = None

        prevNegation = False

        with open("good.txt") as file:
            goodwords = file.read().split()
        file.close()
        with open("bad.txt") as file:
            badwords = file.read().split()
        file.close()
        with open("negations.txt") as file:
            negationwords = file.read().split()
        file.close()
        with open("extensions.txt") as file:
            extensions = file.read().split()
        file.close()

        for message in messages:

            goodSentimentRank = 0

            badSentimentRank = 0

            for word in message:


                if word in goodwords and previousWord in extensions:
                    print("good sentiment detected! But there is a possible negation, the word was: " + Fore.BLACK + Back.GREEN + word + Style.RESET_ALL)

                    #***Detect word negation***
                    if previousWord not in negationwords and prevNegation:
                        print("negation detected! The word: " + Fore.BLACK + Back.GREEN + word + Style.RESET_ALL + " was negated by: " + Fore.BLACK + Back.YELLOW + previousWord + Style.RESET_ALL)

                    else:
                        goodSentimentRank = goodSentimentRank + 1

                    if goodSentimentRank > 5:
                        goodSentimentRank = 5


                elif word in goodwords:
                    print("good sentiment detected! The word was: " + Fore.BLACK + Back.GREEN + word + Style.RESET_ALL)

                    #***Detect word negation***
                    if previousWord in negationwords:
                        print("negation detected! The word: " + Fore.BLACK + Back.GREEN + word + Style.RESET_ALL + " was negated by: " + Fore.BLACK + Back.YELLOW + previousWord + Style.RESET_ALL)
                        prevNegation = False
                    else:
                        goodSentimentRank = goodSentimentRank + 1
                        prevNegation = False

                    if goodSentimentRank > 5:
                        goodSentimentRank = 5

                if word in badwords and previousWord in extensions:
                    print("bad sentiment detected! But there is a possible negation, the word was: " + Fore.BLACK + Back.RED + word + Style.RESET_ALL)

                    # ***Detect word negation***
                    if previousWord not in negationwords and prevNegation:
                        print("negation detected! The word: " + Fore.BLACK + Back.RED + word + Style.RESET_ALL + " was negated by: " + Fore.BLACK + Back.YELLOW + previousWord + Style.RESET_ALL)
                        prevNegation = False
                    else:
                        badSentimentRank = badSentimentRank + 1
                        prevNegation = False

                    if badSentimentRank > 5:
                        badSentimentRank = 5

                    #*****figure this out**************
                    #if word in negationwords:
                    #    prevNegation = True
                    #else:
                    #    previousWord = word

                elif word in badwords:
                    print("bad sentiment detected! The word was: " + Fore.BLACK + Back.RED + word + Style.RESET_ALL)

                    #***Detect word negation***
                    if previousWord in negationwords:
                        print("negation detected! The word: " + Fore.BLACK + Back.RED + word + Style.RESET_ALL + " was negated by: " + Fore.BLACK + Back.YELLOW + previousWord + Style.RESET_ALL)
                        prevNegation = False
                    else:
                        badSentimentRank = badSentimentRank + 1
                        prevNegation = False

                    if badSentimentRank > 5:
                        badSentimentRank = 5



            finalSentiment = goodSentimentRank - badSentimentRank

            user = self.classify_sentiment(finalSentiment)

            self.userSentiment.append(user)




    #*****Takes each users final sentiments and places them into categories*****
    def classify_sentiment(self, sentimentRank):

        if sentimentRank == 5:
            return 'Sentiment: [color=#66ff00]Great![/color]\n'
        if sentimentRank >= 2:
            return 'Sentiment: [color=#4dff4d]Good[/color]\n'
        if sentimentRank >= 0:
            return 'Sentiment: [color=#f1ff00]Neutral[/color]\n'
        if sentimentRank >= -2:
            return 'Sentiment: [color=#ff9999]Bad[/color]\n'
        if sentimentRank == -5:
            return 'Sentiment: [color=#ff0000]Awful[/color]\n'









