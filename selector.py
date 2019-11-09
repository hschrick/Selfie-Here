import hashcrawler
#import kivy
#from kivy.app import App
#from kivy.uix.label import Label
#kivy.require('1.11.1')

class selector():

    def __init__(self, hashName):
        self.hashName = hashName


#Accept user input
def feeder():
    hashName = input("enter desired hashtag ")

    print("enter start time of event yyyy-mm-dd: ")
    since = input()

    print("enter end of time of event yyyy-mm-dd:  ")
    until = input()

    #crawl through the data
    hashcrawler.crawl(hashName, since, until)











