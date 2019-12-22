import kivy
from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.clock import Clock
import kivy.core.text.markup
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.uix.image import AsyncImage
import colorama
from colorama import Fore, Style
import random
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
import time

import twitter_credentials
# import hashcrawler
from hashcrawler import *

import organizer

Builder.load_string("""
<MenuScreen>:
    
    #tagName: tagName.text
    #startTime: startTime.text
    #endTime: endTime.text
    size: 25, 200

    FloatLayout:

        canvas:
        #:import hex kivy.utils.get_color_from_hex
            Color:
                rgb: hex('#512888')
            Rectangle:
                pos:self.pos
                size:self.size

        Image:
            source: "title.png"
            pos_hint:{"center_x":.5,"center_y":.85}


        FloatLayout:
            #cols:2
            size: root.width, root.height

            GridLayout:
                #cols:1
                size_hint: .5, .5
                #pos_hint:{"center_x":.5,"center_y":.5}
                #Label:
                    #text: "TagName: "
                #TextInput:
                    #id: tagName
                    #multiline:False

                #Label:
                    #text: "Start Time: (yyyy-mm-dd-hh-mm-ss) "
                #TextInput:
                    #id: startTime
                    #multiline:False

                #Label:
                    #text: "End Time: (yyyy-mm-dd-hh-mm-ss) "
                #TextInput:
                    #id: endTime
                    #multiline:False
                    
                #Label:
                    #text: "Late time: (yyyy-mm-dd-hh-mm-ss) "
                #TextInput:
                    #id: endTime
                    #multiline:False
                    
                
                 
                #root.tagbtn()         
                #Button:
                    #text: "Submit"
                    #on_press: root.tagbtn()
                    #on_press: root.manager.current = 'results'



<ResultsScreen>:
    cards: cards
    #popmessages: popmessages
    ScrollView:
        

        do_scroll_x: False
        BoxLayout:
            id: cards
            orientation: 'vertical'
            size_hint: (1, None)
      
            
            #Image:
                #source: 'dd.jpeg'
                #pos_hint:{"self.parent.center_x":.5,"self.parent.center_y":.85}
            canvas:
            #:import hex kivy.utils.get_color_from_hex
                Color:
                    rgb: hex('#512888')
                Rectangle:
                    pos:self.pos
                    size:self.size
    
                    
            
                    
            #size_hint: 1, 1   
            
            

<CustomButton@Button>:
    image_source: ''
    subtext: ''
    BoxLayout:
        #canvas:
            #Color:
                #rgba: 1, 0, 0, .5
        pos: self.parent.pos # match the button's position
        cols: 1
        AsyncImage:
            source: root.image_source
            allow_stretch: True
            pos_hint:{"center_x":1.5,"center_y":1.5}
            keep_ratio: True
            size_hint_y: None
            size_hint_x: None
            width: 300
            height: 300
            #font_name: "Roboto-Bold.ttf"
            #font_size: "20"
            
<CustomLabel@Button>:
    
            
#self.newt = Label(text=organizer.popularTweets, pos_hint={"center_x": .5, "center_y": -5},text_size=(self.width+ 600, None), size_hint_y=.01, size_x=60, font_name="Roboto-Bold.ttf", font_size="50")
    
    

            """)


# Declare both screens
class MenuScreen(Screen):
    Window.size = (500, 600)

    def __init__(self, **kwargs):
       super(Screen,self).__init__(**kwargs)
       self.tagbtn()


    tagName = ObjectProperty(None)
    startTime = ObjectProperty(None)
    endTime = ObjectProperty(None)
    lateValue = ObjectProperty(None)
    animationStatus = ObjectProperty(None)

    def tagbtn(self):
        self.add_widget(GridLayout())

        self.cols = 2
        self.tagLabel = Label(text="Tag Name ", pos_hint={"center_x": .5, "center_y": -.1}, font_name="Roboto-Bold.ttf", font_size="40")
        self.add_widget(self.tagLabel)
        self.tagNme = TextInput(multiline=False, size_hint=(.5, .1), pos_hint={"center_x": .5, "center_y": -.2}, text='')

        self.add_widget(self.tagNme)
        self.tostartbtn = Button(text="Next", size_hint=(.5, .1), pos_hint={"center_x": .5, "center_y": -.3})
        self.tostartbtn.bind(on_press=self.startBtn)
        self.add_widget(self.tostartbtn)
        self.locator = Image(source="locator.png", pos_hint={"center_x": .5, "center_y": -.4})
        self.add_widget(self.locator)

        self.tagLabel.opacity = 0;
        self.tagNme.opacity = 0;
        self.tostartbtn.opacity = 0;
        self.locator.opacity = 0;

        anim = Animation(opacity=1, duration=1)
        anim2 = Animation(pos_hint={"center_y": .7}, duration=.5)
        anim3 = Animation(pos_hint={"center_y": .6}, duration=.5)
        anim4 = Animation(pos_hint={"center_y": .47}, duration=.5)
        anim5 = Animation(pos_hint={"center_y": .25}, duration=.5)
        anim.start(self.tagLabel)
        anim.start(self.tagNme)
        anim.start(self.tostartbtn)
        anim.start(self.locator)
        anim2.start(self.tagLabel)
        anim3.start(self.tagNme)
        anim4.start(self.tostartbtn)
        anim5.start(self.locator)



    def startBtn(self, instance):
        self.tagName = self.tagNme.text
        print(self.tagName)


        anim = Animation(pos_hint={"center_x": -1}, duration=.5)
        anim.start(self.tagLabel)
        anim.start(self.tagNme)
        anim.start(self.tostartbtn)
        anim.start(self.locator)

        anim2 = Animation(pos_hint={"center_x": .5}, duration=.5)

        self.startLabel = Label(text="Start Time ", pos_hint={"center_x": 1.5, "center_y": .7}, font_name="Roboto-Bold.ttf", font_size="40")
        self.add_widget(self.startLabel)
        self.strtTime = TextInput(multiline=False, size_hint=(.5, .1), pos_hint={"center_x": 1.5, "center_y": .6}, text='')
        self.add_widget(self.strtTime)
        self.toendbtn = Button(text="Next", size_hint=(.5, .1), pos_hint={"center_x": 1.5, "center_y": .47})
        self.toendbtn.bind(on_press=self.endBtn)
        self.add_widget(self.toendbtn)
        self.startclock = Image(source="clockstart.png", pos_hint={"center_x": 1.5, "center_y": .25})
        self.add_widget(self.startclock)


        anim2.start(self.startLabel)
        anim2.start(self.strtTime)
        anim2.start(self.toendbtn)
        anim2.start(self.startclock)


    def endBtn(self, instance):
        self.startTime = self.strtTime.text
        print(self.startTime)

        anim = Animation(pos_hint={"center_x": -1}, duration=.5)
        anim.start(self.startLabel)
        anim.start(self.strtTime)
        anim.start(self.toendbtn)
        anim.start(self.locator)

        anim2 = Animation(pos_hint={"center_x": .5}, duration=.5)


        self.endLabel = Label(text="End Time ", pos_hint={"center_x": 1.5, "center_y": .7}, font_name="Roboto-Bold.ttf", font_size="40")
        self.add_widget(self.endLabel)
        self.eTime = TextInput(multiline=False, size_hint=(.5, .1), pos_hint={"center_x": 1.5, "center_y": .6}, text='')
        self.add_widget(self.eTime)
        self.tolatebtn = Button(text="Next", size_hint=(.5, .1), pos_hint={"center_x": 1.5, "center_y": .47})
        self.tolatebtn.bind(on_press=self.lteBtn)
        self.add_widget(self.tolatebtn)
        # self.locator = Image(source="locator.png", pos_hint={"center_x": .5, "center_y": .3})
        # self.add_widget(self.locator)

        anim2.start(self.endLabel)
        anim2.start(self.eTime)
        anim2.start(self.tolatebtn)



    def lteBtn(self, instance):
        self.endTime = self.eTime.text
        print(self.endTime)
        anim3 = Animation(pos_hint={"center_y": -.4}, duration=.5)

        anim = Animation(pos_hint={"center_x": -1}, duration=.5)
        anim.start(self.endLabel)
        anim.start(self.eTime)
        anim.start(self.tolatebtn)
        anim.start(self.locator)
        anim3.start(self.startclock)


        anim2 = Animation(pos_hint={"center_x": .5}, duration=.5)

        self.lateLabel = Label(text="late Time ", pos_hint={"center_x": 1.5, "center_y": .7}, font_name="Roboto-Bold.ttf", font_size="40")
        self.add_widget(self.lateLabel)
        self.latetimeL = Label(text="0h ", pos_hint={"center_x": 1.5, "center_y": .55}, font_name="Roboto-Bold.ttf", font_size="75")
        self.add_widget(self.latetimeL)
        self.lateTime = Slider(multiline=False, size_hint=(.5, .1), pos_hint={"center_x": 1.5, "center_y": .47}, min= 0, max= 24, value= 0, cursor_image="cursoredit.png")
        self.lateTime.fbind('value', self.on_slider_val)
        self.add_widget(self.lateTime)
        self.endbtn = Button(text="Next", size_hint=(.5, .1), pos_hint={"center_x": 1.5, "center_y": .3})
        self.endbtn.bind(on_press= self.changer)
        self.add_widget(self.endbtn)
        # self.locator = Image(source="locator.png", pos_hint={"center_x": .5, "center_y": .3})
        # self.add_widget(self.locator)
        anim2.start(self.lateLabel)
        anim2.start(self.latetimeL)
        anim2.start(self.lateTime)
        anim2.start(self.endbtn)
        #anim.start(self.locator)


    #*****Change late time value based on slider movement*****
    def on_slider_val(self, instance, val):
        if val > 10:
            self.latetimeL.text = str(val)[:2] + "h"
            self.lateValue = str(val)[:2]

        else:
            self.latetimeL.text = str(val)[:1] + "h"
            self.lateValue = str(val)[:1]



    def changer(self, *args):
        self.btn()
        self.manager.current = 'results'

    def start(self):
        self.tagbtn()


    def btn(self):
        print(self.tagName, self.startTime, self.endTime)
        self.manager.get_screen('results').build()


class ResultsScreen(Screen):
    main = ObjectProperty()

    def build(self):

        hashcrawler = Hashcrawler()
        # organizer = Organizer()

        main = self.manager.get_screen('menu')
        tagName = main.tagName
        startTime = main.startTime
        endTime = main.endTime
        lateValue = main.lateValue
        #print("late val2 is" + str(lateValue))

        print(tagName + startTime + endTime)

        organizer = hashcrawler.crawl(tagName, startTime, endTime, lateValue)

        # instantiated
        tweetNameList = organizer.tweetNames

        timeAttendedList = organizer.timesAttended

        selfies = organizer.tweetImages

        repeatNames = [];

        # takes attendence of each user and returns proper string color
        # attendeeStatus = organizer.take_attendance(timeAttendedList, startTime, endTime)

        buttons = list(range(len(tweetNameList)))
        images = list(range(len(tweetNameList)))

        self.popularTweets = Label(text="Attendees", size_hint_y=.2, pos_hint={"center_x": .2}, font_name="Roboto-Bold.ttf", font_size="75")
        self.cards.add_widget(self.popularTweets)


        """""
        building cards and adding list data to  them
        """""
        for i in range(len(tweetNameList)):

            # assign selfie from list before placing it into the card below
            selfie = selfies[i]

            if (i == 0):
                throwaway = Factory.CustomButton(text='User: [color=#33FFCA]{}[/color]\n'.format(tweetNameList[0]) + "\n\n" + organizer.take_attendance(timeAttendedList[0], startTime, endTime) + "\n\n" + organizer.userSentiment[0], markup=True, image_source=str(selfies[0]), background_normal='space.png', opacity=.9, font_name="Roboto-Bold.ttf", font_size="30")
                userCard = Factory.CustomButton(text='User: [color=#33FFCA]{}[/color]\n'.format(tweetNameList[0]) + "\n\n" + organizer.take_attendance(timeAttendedList[0], startTime, endTime) + "\n\n" + organizer.userSentiment[0], markup=True, image_source=str(selfies[0]), background_normal='space.png', opacity=.9, font_name="Roboto-Bold.ttf", font_size="30")

                self.h = len(repeatNames)
                self.cards.size = (1, self.h * 450)
                self.cards.add_widget(userCard)
                repeatNames.append(str(selfies[0]))

            else:
                if(str(selfies[i]) not in repeatNames):
                    userCard = Factory.CustomButton(text='User: [color=#33FFCA]{}[/color]\n'.format(tweetNameList[i]) + "\n\n" + organizer.take_attendance(timeAttendedList[i], startTime, endTime) + "\n\n" + organizer.userSentiment[i], markup=True, image_source=str(selfies[i]), background_normal='space.png', opacity=.9, font_name="Roboto-Bold.ttf", font_size="30")

                    self.h = len(repeatNames)
                    self.cards.size = (1, self.h * 400)
                    self.cards.add_widget(userCard)
                    self.cards.spacing = 25
                    repeatNames.append(str(selfies[i]))


        self.popularTweets = Label(text="Popular Sentiment", size_hint_y= .05, pos_hint={ "center_x": .29}, font_name="Roboto-Bold.ttf", font_size="60")
        self.cards.add_widget(self.popularTweets)



        for a in range(len(organizer.popularTweets)):
            userCard = Factory.CustomLabel(text=organizer.popularTweets[a] + '"', text_size=(self.width + 600, None), size_x=60, font_name="Roboto-Bold.ttf", font_size="50", background_normal='mbackground.png')
            self.h = len(repeatNames) + 1
            self.cards.size = (1, self.h * 400)
            self.cards.add_widget(userCard)
            self.cards.spacing = 25

        self.popularTweets = Label(text="Overall Sentiment", size_hint_y=.05, pos_hint={"center_x": .29}, font_name="Roboto-Bold.ttf", font_size="60")
        self.cards.add_widget(self.popularTweets)

        userCard = Factory.CustomLabel(text=str(tagName) + " " + organizer.classify_overall_sentiment(), text_size=(self.width + 600, None), size_x=60, font_name="Roboto-Bold.ttf", font_size="50", markup=True, background_normal='mbackground.png')
        self.h = len(repeatNames) + 3
        self.cards.size = (1, self.h * 400)
        self.cards.add_widget(userCard)
        self.cards.spacing = 25

        #self.popmessages.add_widget(self.newt)

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ResultsScreen(name='results'))


class MyApp(App):
    def build(self):
        return sm



if __name__ == '__main__':
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', -250)
    Config.set('graphics', 'top', 100)
    Config.write()
    MyApp().run()



# root.manager.current = 'results',

