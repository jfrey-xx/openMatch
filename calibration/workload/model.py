#!/usr/bin/python27
# -*- coding: Utf-8 -*
"""Classes du test de calibration pour la reconnaissance de charge de travail pour EEG"""
import sys; sys.path.append('../../lib/lsl') # help python find pylsl relative to this example program
from pylsl import StreamInfo, StreamOutlet, local_clock
import pygame
import random
import time
from pygame.locals import *
from constant import *


class Test:
    """Fonction creant le test initialement"""

    def __init__(self):
        self.chosen = []
        self.list = []
        self.index = 0
        self.time = 0
        self.once = 1
        self.feedback = ""
        self.n_back=0
        self.info = StreamInfo(lsl_name,lsl_type,1,0,lsl_data_type,lsl_id);
        self.outlet = StreamOutlet(self.info);

    """Fonction générant l'interface de test"""


    def generate(self, n_back1):

        self.n_back = n_back1
        #genere le tableau des caracter choisit
        counter = 0
        self.chosen = ['0'] * nb_char
        while counter < nb_char:
            randindex = random.randint(0, len(char_DB)-1)
            if char_DB[randindex] not in self.chosen:
                self.chosen[counter] = char_DB[randindex]
                counter += 1

        self.list = ['0'] * (test_length + self.n_back)
        for i in range(0, len(self.list)):
            randinx = random.randint(0, nb_char)
            self.list[i] = self.chosen[randinx-1]

        self.index = 0
        self.time = 0
        self.string1 = str(self.n_back) + "back-Test"
        self.string2 = "Press the enter key to start test"
        self.string3 = "Press the left mouse button if the character shown is"
        self.string41 = "an " + str(self.chosen[0])
        self.string42 = "the same as " + str(self.n_back) + " characters ago"
        self.string5 = "Press the right mouse button if not"



    """Fonction dessinant l'interface"""


    def draw(self, (width, height), moment, start):
        #variables locales
        font1 = pygame.font.Font(None, primary_fontsize)
        font2 = pygame.font.Font(None, secondary_fontsize)
        #increm = 0

        #redessine l'arrière plan
        background = pygame.Surface((width, height))
        background = background.convert()

        if time.time() < (moment + chartime) and start == 1:
            if self.once == 1:
                    self.once = 0
                    self.clean()
            background.fill((background_grey_color, background_grey_color, background_grey_color))
            text6 = font2.render("", 1, text_color)
            if self.feedback == "right":
                text6 = font2.render("Right", 1, (55, 205, 55))
            elif self.feedback == "wrong":
                text6 = font2.render("Wrong", 1, (230, 40, 30))
            feedpos = text6.get_rect()
            feedpos.midbottom = background.get_rect().midbottom
            background.blit(text6, feedpos)

            #dessinge le text central
            textcentral = font1.render(self.list[self.index], 1, text_color)
            textpos = textcentral.get_rect()
            textpos.center = background.get_rect().center
            background.blit(textcentral, textpos)


        elif start == 0:

            self.once = 1
            text1 = font2.render("This is an "+str(self.n_back)+"-Back Test", 1, text_color)
            text1pos = text1.get_rect()
            text1pos.midtop = background.get_rect().midtop
            background.blit(text1, text1pos)

            text2 = font2.render("Press the Enter key to start the test", 1, text_color)
            text2pos = text2.get_rect()
            text2pos.midbottom = background.get_rect().midbottom
            background.blit(text2, text2pos)

            if self.n_back == 0:
                text3 = font2.render("The target character is : "+str(self.chosen[0]), 1, text_color)
                text3pos = text3.get_rect()
                text3pos.center = background.get_rect().center
                background.blit(text3, text3pos)

        else:
            background.fill(waiting_screen_color)
            text6 = font2.render("", 1, text_color)
            if self.feedback == "right":
                text6 = font2.render("Right", 1, (55, 205, 55))
            elif self.feedback == "wrong":
                text6 = font2.render("Wrong", 1, (230, 40, 30))
            feedpos = text6.get_rect()
            feedpos.midbottom = background.get_rect().midbottom
            background.blit(text6, feedpos)
        #retourn l'image à afficher
        return background


    def action(self, action_type, pic):
        if action_type == "true":
            self.outlet.push_sample([PLAYER_RIGHT_ANSWER]) 
            if self.n_back == 0 and self.list[self.index+pic] == self.chosen[0]:
                self.feedback = "right"
                self.outlet.push_sample([SYSTEM_RIGHT_ANSWER])
            elif self.n_back != 0 and self.list[self.index+pic] == self.list[self.index+pic - self.n_back]:
                self.feedback = "right"
                self.outlet.push_sample([SYSTEM_RIGHT_ANSWER])                
            else:
                self.feedback = "wrong"
                self.outlet.push_sample([SYSTEM_WRONG_ANSWER])
        elif action_type == "false":
            self.outlet.push_sample([PLAYER_WRONG_ANSWER])
            if self.n_back == 0 and self.list[self.index+pic] == self.chosen[0]:
                self.feedback = "wrong"
                self.outlet.push_sample([SYSTEM_WRONG_ANSWER])
            elif self.n_back != 0 and self.list[self.index+pic] == self.list[self.index+pic - self.n_back]:
                self.feedback = "wrong"
                self.outlet.push_sample([SYSTEM_WRONG_ANSWER])
            else:
                self.feedback = "right"
                self.outlet.push_sample([SYSTEM_RIGHT_ANSWER])
        else:
            self.feedback = ""


    def next(self, newindex):
        self.index = newindex
        self.feedback = ""

    def clean(self):
        self.feedback = ""

    def tutorial(self):
        return 0