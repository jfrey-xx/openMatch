#!/usr/bin/python27
# -*- coding: Utf-8 -*
"""Constantes pour le test de calibration pour la reconnaissance de charge de travail"""
#Paramètre LSL
lsl_name='MazenergyMarkers'
lsl_type='Markers'
lsl_data_type='int32'
lsl_id = '101187'
debug_fps_latency=1
fullscreen_flag=0
PLAYER_RIGHT_ANSWER=1
PLAYER_WRONG_ANSWER=2
SYSTEM_RIGHT_ANSWER=3
SYSTEM_WRONG_ANSWER=4
SYSTEM_DARKTIME=5
SYSTEM_BEGIN_TRIAL_0BACK=6
SYSTEM_BEGIN_TRIAL_2BACK=7
SYSTEM_BEGIN_SESSION=8
SYSTEM_END_SESSION=9
#Paramètre fenêtre
initial_screen_height = 480			# taille verticale initiale de la fenêtre
initial_screen_width = 640			# taille horizontale initiale de la fenêtre
background_grey_color = 0			# couleur de gris de la l'arrière plan de la fenêtre
primary_fontsize = 300				# taille de la police utilisé lors de l'expérience
secondary_fontsize = 50 			# taille de la police pour le text explicatif
text_color = (255, 255, 255)	    # couleur du text à afficher
waiting_screen_color = (0,0,0)      # couleur de l'écran d'attente

#Paramètres expérience
char_DB = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z']
nb_char = 4							# nombre de caractère différent utilisé pendant le test 
test_length = 60					    # nombre de signe utile à l'expérience
timed = 0							# est-ce que l'expérience est chronometré
wait_time = 1						# temps d'attente en seconde
chartime = 0.5						# temps d'affichae de chaque caractere en seconde
blacktime = 1.5					    # temps de pause entre chaque caractere en seconde
tutorial_presence = 0              # presence d'une démontration avant le début de l'expérience
#Paramètere de sessions
#session_list = [0, 2, 0, 2, 2, 0, 0, 0, 2, 2] #série d'expérience effectué
session_size = 6
