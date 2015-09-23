#!/usr/bin/python27
# -*- coding: Utf-8 -*

"""
Programme pour reconnaissance de charge de travail mesur�e par casque EEG
Programme proposant une calibration de casque EEG afin d'obtenir de meilleurs r�sultats dans le futur

Inspiree par le test standard N-back

Script Python
Fichiers inclus : constant.py, classes.py
"""

#importation de ressources
import pygame
import random
import time
import numpy
import socket
from pygame.locals import *
from constant import *
from model import *
import numpy as np


#Initialisation des variables
proceed = 1
test_over = 1
test_start = 0
screen_height = initial_screen_height
screen_width = initial_screen_width
dark_time = time.time()
test_time = 0
send_darktime_stimulus = 1
choose=0
this_test = Test()

session_list = [0]*session_size
indice = np.random.randint(0,2)
if indice == 1 :
    session_list[0] = indice
    for i in range(1,len(session_list)) :
        session_list[i] = (i+1)%2
if indice == 0 :
    session_list[0] = indice
    for i in range(1,len(session_list)) :
        session_list[i] = i%2
        
for i in range(len(session_list)) :
    if session_list[i]== 1:
        session_list[i]=2
session_index = 0
n_back = session_list[session_index]
test_number = test_length + n_back

#Initialisation du moteur de jeu/graphique
pygame.init()
mode = RESIZABLE
if fullscreen_flag == 1:
    mode = FULLSCREEN
screen = pygame.display.set_mode((initial_screen_width, initial_screen_height), mode)
pygame.display.set_caption('Calibration charge de travail')

# Dessine l'arriere plan dans un premier temps
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((background_grey_color, background_grey_color, background_grey_color))
# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

while this_test.outlet.have_consumers() == False and debug_fps_latency == 1 :
    continue

while proceed:

    if test_over != 0:
        test_number += 1
        if test_number >= test_length + n_back:
            if session_index < len(session_list):
                n_back = session_list[session_index]
                this_test.generate(n_back)
                test_over = 0
                send_darktime_stimulus = 1
                choose=0
                test_start = 0
                test_number = 0
                session_index += 1
                this_test.outlet.push_sample([SYSTEM_BEGIN_SESSION])
                dark_time = time.time()
                continue
            else:
                proceed = 0
                continue
        else:
            this_test.next(test_number)
            if n_back == 0:
                this_test.outlet.push_sample([SYSTEM_BEGIN_TRIAL_0BACK])
            elif n_back == 2: 
                this_test.outlet.push_sample([SYSTEM_BEGIN_TRIAL_2BACK])
            dark_time = time.time()
            test_over = 0
            send_darktime_stimulus = 1
            choose=0

    for event in pygame.event.get():

        #presence d'un tutoriel initial
        if tutorial_presence == 1:
            tutorial_presence = this_test.tutorial()
            continue

        if event.type == KEYDOWN and event.key == K_RETURN:
            test_start = 1
            this_test.outlet.push_sample([SYSTEM_BEGIN_SESSION])
            dark_time = time.time()

        if test_number >= n_back and test_start == 1:
            if event.type == MOUSEBUTTONDOWN and choose==0:
                if event.button == 1:
                        this_test.action("true", 0)
                        choose=1
                        #this_test.action("", 0)
                elif event.button == 3:
                        this_test.action("false", 0)
                        choose=1
                        #this_test.action("", 0)

        if event.type == VIDEORESIZE:
            screen_height = event.h
            screen_width = event.w
            screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            proceed = 0
    
    if time.time() >= dark_time + chartime and test_start == 1 and send_darktime_stimulus == 1:
        this_test.outlet.push_sample([SYSTEM_DARKTIME])
        send_darktime_stimulus = 0
        
    if time.time() >= (dark_time + chartime + blacktime) and test_start == 1:
        test_over = 1

    background = this_test.draw((screen_width, screen_height), dark_time, test_start)
    screen.fill((background_grey_color, background_grey_color, background_grey_color))
    screen.blit(background, (0, 0))
    pygame.display.flip()
this_test.outlet.push_sample([SYSTEM_END_SESSION])
pygame.quit()
sys.exit()
