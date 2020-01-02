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
        self.popularTweets = []
        self.overallSentiment = []
        self.lateTime = 0

    def organize(self, tweetTime, tweetMessage, tweetAttendanceStart, tweetAttendanceEnd, tweetName, timage, rtList, fList, lateValue):

        self.tweetNames = tweetName

        self.messages = tweetMessage
        self.lateTime = lateValue

        self.timesAttended = tweetTime
        self.take_attendance(self.timesAttended, tweetAttendanceStart, tweetAttendanceEnd)

        self.tweetImages = timage

        self.retweetList = rtList

        self.favoriteList = fList

        self.popularTweets = self.find_popular_tweets()

        self.message_clipper()

        self.classify_overall_sentiment()

    # **********combines retweets and favorites of each user and finds the most popular**********
    def find_popular_tweets(self):

        rtlist = self.retweetList
        fvlist = self.favoriteList
        popularUser = 0
        popularUsertwo = 0
        popularUserthree = 0
        popularcount = 0
        popularMessages = self.messages
        popularmessage = ""
        popularmessagetwo = ""
        popularmessagethree = ""
        popularCleanMessages = []

        cleanMessages = self.popular_message_clipper()

        print(self.favoriteList)


        #users = rtlist

        #for i in users:
               # users[i] += fvlist[i]

        users = []
        for i in range(0, len(rtlist)):
            users.append(rtlist[i] + fvlist[i])

        print(users)


        for i in users:
            print("this tweet is: " + str(i))
        # **********Combine rts and likes for each user**********


        #filter out the most popular tweets

        length = len(users)

        #users.sort();



        index = list(range(len(users)))

        index.sort(key=users.__getitem__)

        users[:] = [users[i] for i in index]
        cleanMessages[:] = [cleanMessages[i] for i in index]
        print(cleanMessages[users[length - 1]])
        print(cleanMessages)


        popularUser = cleanMessages[length - 1]    #users[length - 1]
        print("     most pop: " + str(cleanMessages[length - 1]))

        popularUsertwo = cleanMessages[length - 2]
        print("    2nd most pop: " + str(cleanMessages[length - 2]))

        popularUserthree = cleanMessages[length - 3]
        print("    3rd most pop: " + str(cleanMessages[length - 3]))


        if(users[length - 1] > 0):
            popularmessage = self.string_convert(popularUser)
            popularCleanMessages.append(popularmessage)

        if (users[length - 2] > 0):
            popularmessagetwo = self.string_convert(popularUsertwo)
            popularCleanMessages.append(popularmessagetwo)

        if (users[length - 3] > 0):
            popularmessagethree = self.string_convert(popularUserthree)
            popularCleanMessages.append(popularmessagethree)

        #*****DEBUG FOR TESTING ONLY*****
        #print("The most popular message is: " + str(cleanMessages[popularUser]))
        #print("The 2nd most popular message is: " + str(cleanMessages[popularUsertwo]))
        #print("The 3rd most popular message is: " + str(cleanMessages[popularUserthree]))
        #print("The most popular tweet is: " + str(max))

        return popularCleanMessages




    def popular_message_clipper(self):

        cleanMessages = []

        for i in self.messages:
            dirtyMessage = i.split()

            #**remove name, tag, and username and img link**


            if "@" in dirtyMessage:
                dirtyMessage.pop(0)
            dirtyMessage.pop(0)
            dirtyMessage.insert(0, '"')
            del dirtyMessage[-1]
            cleanMessages.append(dirtyMessage)


        return cleanMessages


    #*****Converts lists into a single string*****
    def string_convert(self, s):
        newString = ""

        for i in s:
            newString += i + " "

        return newString



    """""
    compares times attended with expected attendance and colors accordingly.
    """""
    def take_attendance(self, tAttended, tweetAttendanceStart, tweetAttendanceEnd):

        #clean up custom start time
        tweetAttendanceStart = str(tweetAttendanceStart)
        newStart = tweetAttendanceStart.strip()
        newStart = newStart.replace("-", "")
        newStart = newStart.replace(":", "")

        print("the start time is: " + str(newStart))


        #clean up custom end time
        newEnd = tweetAttendanceEnd.replace(" ", "")
        newEnd = newEnd.replace("-", "")
        newEnd = newEnd.replace(":", "")

        print("the end time is: " + str(newEnd))



        # clean up each attendents time
        tAttended = str(tAttended)


        # hourStart = ""
        hoursAttended = tAttended.split()
        testattend = hoursAttended[1]
        #print(str(testattend))
        #print(testattend[:2])
        cleanTime = self.convert_time(testattend)

        finalUserTime = str(hoursAttended[0] + " " + cleanTime)
        #print(finalUserTime)

        newtime = tAttended.replace(" ", "")
        newtime = newtime.replace("-", "")
        newtime = newtime.replace(":", "")

        print("the user time is: " + str(newtime))
        #print("the hour strip is: " + str(testattend))

        self.clean_lateval()

        #build a comparison to test for lateness
        late = str(str(newStart) + str(self.lateTime))

        #*****FOR DEBUG ONLY*****
        #print("FINAL NEW TIME: " + newtime)
        #print("FINAL LATE TIME: " + late)
        #print("FINAL START TIME: " + newStart)
        #print("FINAL END TIME: " + newEnd)
        #compare user time with start time and end time
        if (newtime >= late and newtime <= newEnd):
            return 'Time: [color=#ff0000]{}[/color]\n'.format(finalUserTime)
        if(newtime >= newStart and newtime <= newEnd):
            return 'Time: [color=#7CFC00]{}[/color]\n'.format(finalUserTime)


    def clean_lateval(self):

        if(len(self.lateTime) == 1):
            self.lateTime = "0" + self.lateTime + "0000"
        if (len(self.lateTime) == 2):
            self.lateTime = self.lateTime + "0000"


    #*****Sentiment Analyzer*****
    def convert_time(self, testattend):
        #timeArray = testattend.split(':')
        hour = int(testattend[:2])
        #print("success: " + str(testattend))

        ampm = ""
        if hour == 12:
            ampm = "PM"
        elif hour == 0:
            ampm = "AM"
            hours = 12
        elif hour >= 12:
            ampm = "PM"
            hour = int(hour) - 12
        else:
            ampm = "AM"

        #print(str(hour) + ":" + ampm)
        finalTime = testattend.replace(str(testattend[:2]), str(hour)) + ampm
        #print("this is the final " + finalTime)
        return finalTime

    #*****Cleans up tweets into message blocks*****
    def message_clipper(self):

        cleanMessages = []

        for i in self.messages:
            dirtyMessage = i.split()
            dirtyMessage.pop(0)
            del dirtyMessage[-1]
            cleanMessages.append(dirtyMessage)

        self.detect_sentiment(cleanMessages)

        #print("message is " + str(cleanMessages[0]))

    #*****Ajusts and sets sentiment ranks for each user*****
    def detect_sentiment(self, messages):

        finalSentiment = 0

        previousWord = None

        prevExtension = None

        prevNegation = None

        wordBehindNegation = None

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
                    if previousWord not in negationwords and negationPresent:
                        print("negation detected! The word: " + Fore.BLACK + Back.GREEN + word + Style.RESET_ALL + " was negated by: " + Fore.BLACK + Back.YELLOW + prevNegation + Style.RESET_ALL)

                    else:
                        goodSentimentRank = goodSentimentRank + 1

                    if goodSentimentRank > 5:
                        goodSentimentRank = 5

                elif word in goodwords:
                    print("good sentiment detected! The word was: " + Fore.BLACK + Back.GREEN + word + Style.RESET_ALL)

                    #***Detect word negation***
                    if wordBehindNegation in negationwords:
                        print("negation detected! The word: " + Fore.BLACK + Back.GREEN + word + Style.RESET_ALL + " was negated by: " + Fore.BLACK + Back.YELLOW + wordBehindNegation + Style.RESET_ALL)
                        negationPresent = False
                    else:
                        goodSentimentRank = goodSentimentRank + 1
                        negationPresent = False

                    if goodSentimentRank > 5:
                        goodSentimentRank = 5


                if word in badwords and previousWord in extensions:
                    print("bad sentiment detected! But there is a possible negation, the word was: " + Fore.BLACK + Back.RED + word + Style.RESET_ALL)

                    # ***Detect word negation***
                    if previousWord not in negationwords and prevNegation:
                        print("negation detected! The word: " + Fore.BLACK + Back.RED + word + Style.RESET_ALL + " was negated by: " + Fore.BLACK + Back.YELLOW + prevNegation + Style.RESET_ALL)
                        negationPresent = False
                    else:
                        badSentimentRank = badSentimentRank + 1
                        negationPresent = False

                    if badSentimentRank > 5:
                        badSentimentRank = 5


                elif word in badwords:
                    print("bad sentiment detected! The word was: " + Fore.BLACK + Back.RED + word + Style.RESET_ALL)

                    #***Detect word negation***
                    if wordBehindNegation in negationwords:
                        print("negation detected! The word: " + Fore.BLACK + Back.RED + word + Style.RESET_ALL + " was negated by: " + Fore.BLACK + Back.YELLOW + wordBehindNegation + Style.RESET_ALL)
                        negationPresent = False
                    else:
                        badSentimentRank = badSentimentRank + 1
                        negationPresent = False

                    if badSentimentRank > 5:
                        badSentimentRank = 5

            #*****Store previous words as needed as negations or extensions*****
                if word in negationwords:
                    negationPresent = True
                    prevNegation = word
                else:
                    previousWord = word

                wordBehindNegation = word



            #*****Declare final sentiments and apply them to each user******
            finalSentiment = goodSentimentRank - badSentimentRank

            user = self.classify_sentiment(finalSentiment)
            self.overallSentiment.append(finalSentiment)

            self.userSentiment.append(user)

           #self.store_in_bank(messages)



    #*****clean up and store messages for training*****
   # def store_in_bank(self, messages):
    #    fullMessages = messages
    #    for message in messages:

      #      finalMessage = self.string_convert(message)

     #       for word in finalMessage:
     #           if word.isupper():
     #               print("ignore")
     #           else:
     #               print("found")







    #*****Takes each users final sentiments and places them into categories*****
    def classify_sentiment(self, sentimentRank):

        if sentimentRank >= 4:
            return 'Sentiment: [color=#66ff00]Great![/color]\n'
        if sentimentRank >= 2:
            return 'Sentiment: [color=#4dff4d]Good[/color]\n'
        if sentimentRank >= 0:
            return 'Sentiment: [color=#f1ff00]Neutral[/color]\n'
        if sentimentRank >= -2:
            return 'Sentiment: [color=#ff9999]Bad[/color]\n'
        if sentimentRank >= -5:
            return 'Sentiment: [color=#ff0000]Awful[/color]\n'

    def classify_overall_sentiment(self):
        totalSentiment = 0

        for sentiment in self.overallSentiment:
            #print("sentiment is: " + str(sentiment))
            totalSentiment += sentiment
            #print("the total sentiment is: " + str(totalSentiment))

        self.classify_sentiment(totalSentiment)
        #print("the total sentiment is: " + str(totalSentiment))

        if totalSentiment >= 5:
            return 'was a [color=#66ff00]great[/color] event!\n'
        if totalSentiment >= 2:
            return 'was a [color=#4dff4d]good[/color] event!\n'
        if totalSentiment >= 0:
            return 'was a [color=#f1ff00]neutral[/color] event.\n'
        if totalSentiment >= -2:
            return 'was a [color=#ff9999]bad[/color] event.\n'
        if totalSentiment <= -5:
            return 'was a [color=#ff0000]awful[/color] event.\n'











