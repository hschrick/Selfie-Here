import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
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
import kivy.core.text.markup
from kivy.factory import Factory
from kivy.uix.image import AsyncImage
import colorama
from colorama import Fore, Style
import random
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler


import twitter_credentials
#import hashcrawler
from hashcrawler import *

import organizer

Builder.load_string("""
<MenuScreen>:
    tagName: tagName.text
    startTime: startTime.text
    endTime: endTime.text
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
            cols:1
            size: root.width, root.height
        
            GridLayout:
                cols:1
                size_hint: .5, .5
                pos_hint:{"center_x":.5,"center_y":.5}

                Label:
                    text: "TagName: "

                TextInput:
                    id: tagName
                    multiline:False
                    

                Label:
                    text: "Start Time: "

                TextInput:
                    id: startTime
                    multiline:False
                
                Label:
                    text: "End Time: "

                TextInput:
                    id: endTime
                    multiline:False

                Button:
                    text: "Submit"
                    on_press: root.btn()
                    on_press: root.manager.current = 'results'
           
            
            

<ResultsScreen>:
    cards: cards
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
            
            
                
            """)




# Declare both screens
class MenuScreen(Screen):
    Window.size = (500, 600)

    tagName = ObjectProperty(None)
    startTime = ObjectProperty(None)
    endTime = ObjectProperty(None)


    def btn(self):
        print(self.tagName, self.startTime, self.endTime)
        self.manager.get_screen('results').show_names()





class ResultsScreen(Screen):
    main = ObjectProperty()


    def show_names(self):

        hashcrawler = Hashcrawler()
        #organizer = Organizer()

        main = self.manager.get_screen('menu')
        tagName = main.tagName
        startTime = main.startTime
        endTime = main.endTime

        print(tagName + startTime + endTime)

        organizer = hashcrawler.crawl(tagName, startTime, endTime)



        #instantiated
        tweetNameList = organizer.tweetNames

        timeAttendedList = organizer.timesAttended

        selfies = organizer.tweetImages

        #takes attendence of each user and returns proper string color
        #attendeeStatus = organizer.take_attendance(timeAttendedList, startTime, endTime)

        buttons = list(range(len(tweetNameList)))
        images = list(range(len(tweetNameList)))


        """""
        building cards and adding list data to  them
        """""
        for i in range(len(tweetNameList)):
            #assign selfie from list before placing it into the card below
            selfie = selfies[i]

            if(i == 0):
                throwaway = Factory.CustomButton(text='User: [color=#33FFCA]{}[/color]\n'.format(tweetNameList[0]) + "\n\n" + organizer.take_attendance(timeAttendedList[0], startTime, endTime) + "\n\n" + organizer.userSentiment[0], markup=True, image_source=str(selfies[0]), background_normal='space.png')
                userCard = Factory.CustomButton(text='User: [color=#33FFCA]{}[/color]\n'.format(tweetNameList[0]) + "\n\n" + organizer.take_attendance(timeAttendedList[0], startTime, endTime) + "\n\n" + organizer.userSentiment[0], markup=True, image_source=str(selfies[0]), background_normal='space.png')

                self.h = len(tweetNameList)
                self.cards.size = (1, self.h * 450)
                self.cards.add_widget(userCard)
            else:
                userCard = Factory.CustomButton(text='User: [color=#33FFCA]{}[/color]\n'.format(tweetNameList[i]) + "\n\n" + organizer.take_attendance(timeAttendedList[i], startTime, endTime) + "\n\n" + organizer.userSentiment[i] , markup=True, image_source=str(selfies[i]), background_normal='space.png')

                self.h = len(tweetNameList)
                self.cards.size = (1, self.h * 400)
                self.cards.add_widget(userCard)
                self.cards.spacing = 25


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ResultsScreen(name='results'))



class MyApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()



#root.manager.current = 'results',

