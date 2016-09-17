#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Project           : Kanpani Girls
#
# File name         : kanpani_girls.py
#
# Author            : Cheang Shian Chin
#
# Date created      : 13 Aug 2016
#
# Purpose           : Play Kanpani Girls using pyautogui.
#
#----------------------------------------------------------------------


import logging
import os
import pyautogui
import random
import time

# various coordinates of objects in the game
GAME_REGION = () # (left, top, width, height) values coordinates of the entire game window
CENTER_COORDS = None
PLAY_BUTTON_COORDS = None
FACILITIES_BUTTON_COORDS = None
CHAR_STORY_COORDS = None
CHAR_STORY_UP_ARROW_COORDS = None
CHAR_STORY_HOLLY_COORDS = None
CHAR_STORY_EP1_COORDS = None
CHAR_STORY_BEGIN_STORY_COORDS = None
PARTY_BEGIN_STORY_COORDS = None
FAST_FORWARD_BUTTON_COORDS = None
CHAPTER_ONE_BUTTON_COORDS = None
SLOT_2_BUTTON_COORDS = None    # slot 1 is the bottom one
ACCEPT_QUEST_BUTTON_COORDS = None
EQUIPMENT_LAB_COORDS = None
CLERIC_EQUIP_COORDS = None
EQUIP_UP_ARROW_COORDS = None
EQUIP_SLOT_2_COORDS = None  # slot 1 is the bottom one
DEVELOP_BIG_COORDS = None
DEVELOP_SMALL_COORDS = None
CONTINUE_RESEARCH_COORDS = None
CLOSE_COORDS = None # close continue research
TOP_LEFT_BUTTON_COORDS = None
CLOSE_NO_FOOD_BUTTON_COORDS = None

# Page constants
PLAY_PAGE = 'play'
FACILITIES_PAGE = 'facilities'
EQUIP_DEV_PAGE = 'equipment_development'
CHAR_STORY_PAGE = 'char_story'
QUEST_RESULT_PAGE = 'quest_end'
CEO_OFFICE_PAGE = 'ceo_office'
QUEST_ONGOING_PAGE = 'quest_on_going'
INTERDIMENSIONAL_GIRLS_PAGE = 'interdimensional_girls'
CONTINUE_RESEARCH_PAGE = 'continue_research'
FOOD_NOT_ENOUGH = 'not_enough_food'

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
    #logging.disable(logging.INFO) # uncomment to block info log messages

    """Runs the entire program. The Kanpani Girls game must be visible on the screen and the PLAY button visible."""
    logging.info('Program Started. Press Ctrl-C to abort at any time.')
    logging.info('To interrupt mouse movement, move mouse to upper left corner.')

    getGameRegion()
    setupCoordinates()
    count = 0
    while True:
        count += 1
        logging.info('Round %d', count)
        #developEquipments()
        #startMainQuests()
        #count += 1
        startHollyQuests()



def getGameStatus(to_find):
    '''Use this function to find the expected page/state/status the game is now in'''
    found = None

    if to_find == CEO_OFFICE_PAGE:
        found = pyautogui.locateOnScreen(imgPath("CeoOffice.png")
            , region=(GAME_REGION[0], GAME_REGION[1]+GAME_REGION[3]-115, GAME_REGION[2]+115, GAME_REGION[3]+115))
        if found: logging.info('CEO Office page...')

    elif to_find == CHAR_STORY_PAGE:
        found = pyautogui.locateOnScreen(imgPath("char_story_home.png")
            , region=(GAME_REGION[0]+60, GAME_REGION[1]+95, GAME_REGION[2]+200, GAME_REGION[3]+50))
        if found: logging.info('Character Story page...')

    elif to_find == INTERDIMENSIONAL_GIRLS_PAGE:
        found = pyautogui.locateOnScreen(imgPath("interdimensional_girls.png")
            , region=(GAME_REGION[0]+125, GAME_REGION[1]+100, GAME_REGION[2]+130, GAME_REGION[3]+50))
        if found: logging.info('Chapter 1 - Interdimensional Girls page...')

    elif to_find == PLAY_PAGE:
        found = pyautogui.locateOnScreen(imgPath("playPage.png")
            , region=(GAME_REGION[0]+185, GAME_REGION[1]+120, GAME_REGION[2]+80, GAME_REGION[3]+55))
        if found: logging.info('Play page...')

    elif to_find == EQUIP_DEV_PAGE:
        found = pyautogui.locateOnScreen(imgPath("fighter_equip.png"), region=GAME_REGION)
        if found: logging.info('Facilities page...')

    elif to_find == QUEST_RESULT_PAGE:
        found = pyautogui.locateOnScreen(imgPath("quest_results.png"), region=GAME_REGION)
        if found: logging.info('Quest ended...')

    elif to_find == QUEST_ONGOING_PAGE:
        found = pyautogui.locateOnScreen(imgPath("quest_on_going.png")
            , region=(GAME_REGION[0]+170, GAME_REGION[1], GAME_REGION[2]+50,GAME_REGION[3]+30))
        if found: logging.info('Quest on going...')

    elif to_find == FOOD_NOT_ENOUGH:
        found = pyautogui.locateOnScreen(imgPath("not_enough_food.png"), region=GAME_REGION)
        if found: logging.info('Not enough food...')

    elif to_find == CONTINUE_RESEARCH_PAGE:
        found = pyautogui.locateOnScreen(imgPath("continue_research.png"), region=GAME_REGION)
        if found: logging.info('Continue to research?...')

    else:
        logging.info('Unknown status...')
        pass

    if not found: logging.info('{} not found.'.format(to_find))
    return found

def getGameRegion():
    """Obtains the region that the Kanpani Girls game is on the screen and assigns it to GAME_REGION.
       The game must be at the start screen (where the PLAY button is visible)."""
    global GAME_REGION

    # identify the CEO Office
    logging.info('Finding game region...')
    region = pyautogui.locateOnScreen(imgPath("CeoOffice.png"))
    while region is None:
        logging.info('Could not find game on screen. Is the game visible?')
        time.sleep(5)
        getGameRegion()
        #raise Exception('Could not find game on screen. Is the game visible?')

    # calculate the region of the entire game
    bottomLeftX = region[0] # left
    bottomLeftY = region[1] + region[3] # bottom + width
    GAME_REGION = (bottomLeftX, bottomLeftY-590, 950, 590) # the game screen is always 950 x 590
    logging.info('Game region found: %s' % (GAME_REGION,))

def setupCoordinates():
    """Sets several of the coordinate-related global variables, after acquiring the value for GAME_REGION."""
    global CENTER_COORDS
    global PLAY_BUTTON_COORDS
    global FACILITIES_BUTTON_COORDS
    global CHAR_STORY_COORDS
    global CHAR_STORY_UP_ARROW_COORDS
    global CHAR_STORY_HOLLY_COORDS
    global CHAR_STORY_EP1_COORDS
    global CHAR_STORY_BEGIN_STORY_COORDS
    global PARTY_BEGIN_STORY_COORDS
    global FAST_FORWARD_BUTTON_COORDS
    global CHAPTER_ONE_BUTTON_COORDS
    global SLOT_2_BUTTON_COORDS
    global ACCEPT_QUEST_BUTTON_COORDS
    global EQUIPMENT_LAB_COORDS
    global CLERIC_EQUIP_COORDS
    global EQUIP_UP_ARROW_COORDS
    global EQUIP_SLOT_2_COORDS
    global DEVELOP_BIG_COORDS
    global DEVELOP_SMALL_COORDS
    global CONTINUE_RESEARCH_COORDS
    global CLOSE_COORDS
    global TOP_LEFT_BUTTON_COORDS
    global CLOSE_NO_FOOD_BUTTON_COORDS

    CENTER_COORDS = (GAME_REGION[0] + GAME_REGION[2]/2, GAME_REGION[1] + GAME_REGION[3]/2)
    PLAY_BUTTON_COORDS = (GAME_REGION[0] + 275, GAME_REGION[1] + 330)
    FACILITIES_BUTTON_COORDS = (GAME_REGION[0] + 170, GAME_REGION[1] + 180)
    CHAR_STORY_COORDS = (GAME_REGION[0] + 910, GAME_REGION[1] + 100)
    CHAR_STORY_UP_ARROW_COORDS = (GAME_REGION[0] + 170, GAME_REGION[1] + 150)
    CHAR_STORY_HOLLY_COORDS = (GAME_REGION[0] + 170, GAME_REGION[1] + 280)
    CHAR_STORY_EP1_COORDS = (GAME_REGION[0] + 500, GAME_REGION[1] + 270)
    CHAR_STORY_BEGIN_STORY_COORDS = (GAME_REGION[0] + 810, GAME_REGION[1] + 525)
    PARTY_BEGIN_STORY_COORDS = (GAME_REGION[0] + 400, GAME_REGION[1] + 400)
    FAST_FORWARD_BUTTON_COORDS = (GAME_REGION[0] + 930, GAME_REGION[1] + 452)
    CHAPTER_ONE_BUTTON_COORDS = (GAME_REGION[0] + 170, GAME_REGION[1] + 280)
    SLOT_2_BUTTON_COORDS = (GAME_REGION[0] + 170, GAME_REGION[1] + 485)
    ACCEPT_QUEST_BUTTON_COORDS = (GAME_REGION[0] + 900, GAME_REGION[1] + 435)
    EQUIPMENT_LAB_COORDS = (GAME_REGION[0] + 230, GAME_REGION[1] + 400)
    CLERIC_EQUIP_COORDS = (GAME_REGION[0] + 265, GAME_REGION[1] + 180)
    EQUIP_UP_ARROW_COORDS = (GAME_REGION[0] + 90, GAME_REGION[1] + 230)
    EQUIP_SLOT_2_COORDS = (GAME_REGION[0] + 175, GAME_REGION[1] + 410)
    DEVELOP_BIG_COORDS = (GAME_REGION[0] + 440, GAME_REGION[1] + 560)
    DEVELOP_SMALL_COORDS = (GAME_REGION[0] + 420, GAME_REGION[1] + 480)
    CONTINUE_RESEARCH_COORDS = (GAME_REGION[0] + 415, GAME_REGION[1] + 445)
    CLOSE_COORDS = (GAME_REGION[0] + 535, GAME_REGION[1] + 445)
    TOP_LEFT_BUTTON_COORDS = (GAME_REGION[0] + 50, GAME_REGION[1] + 40)
    CLOSE_NO_FOOD_BUTTON_COORDS = (GAME_REGION[0] + 475, GAME_REGION[1] + 390)

    logging.info('CENTER_COORDS: %s' % (CENTER_COORDS,))
    logging.info('PLAY_BUTTON_COORDS: %s' % (PLAY_BUTTON_COORDS,))
    logging.info('FACILITIES_BUTTON_COORDS: %s' % (FACILITIES_BUTTON_COORDS,))
    logging.info('CHAR_STORY_COORDS: %s' % (CHAR_STORY_COORDS,))
    logging.info('CHAR_STORY_UP_ARROW_COORDS: %s' % (CHAR_STORY_UP_ARROW_COORDS,))
    logging.info('CHAR_STORY_HOLLY_COORDS: %s' % (CHAR_STORY_HOLLY_COORDS,))
    logging.info('CHAR_STORY_EP1_COORDS: %s' % (CHAR_STORY_EP1_COORDS,))
    logging.info('CHAR_STORY_BEGIN_STORY_COORDS: %s' % (CHAR_STORY_BEGIN_STORY_COORDS,))
    logging.info('PARTY_BEGIN_STORY_COORDS: %s' % (PARTY_BEGIN_STORY_COORDS,))
    logging.info('FAST_FORWARD_BUTTON_COORDS: %s' % (FAST_FORWARD_BUTTON_COORDS,))
    logging.info('CHAPTER_ONE_BUTTON_COORDS: %s' % (CHAPTER_ONE_BUTTON_COORDS,))
    logging.info('SLOT_2_BUTTON_COORDS: %s' % (SLOT_2_BUTTON_COORDS,))
    logging.info('ACCEPT_QUEST_BUTTON_COORDS: %s' % (ACCEPT_QUEST_BUTTON_COORDS,))
    logging.info('EQUIPMENT_LAB_COORDS: %s' % (EQUIPMENT_LAB_COORDS,))
    logging.info('CLERIC_EQUIP_COORDS: %s' % (CLERIC_EQUIP_COORDS,))
    logging.info('EQUIP_UP_ARROW_COORDS: %s' % (EQUIP_UP_ARROW_COORDS,))
    logging.info('EQUIP_SLOT_2_COORDS: %s' % (EQUIP_SLOT_2_COORDS,))


def developEquipments():
    # Start from CEO Office
    logging.info('Looking for Facilities button...')
    #while (getCurrentPage() != FACILITIES_PAGE):
    pyautogui.click(FACILITIES_BUTTON_COORDS, duration=0.25)
    time.sleep(5)

    logging.info('Clicked on Facilities button.')

    time.sleep(1)
    pyautogui.click(EQUIPMENT_LAB_COORDS, duration=0.25)
    time.sleep(3)
    pyautogui.click(EQUIPMENT_LAB_COORDS, duration=0.25)    # click "develop equipment"

    while not getGameStatus(EQUIP_DEV_PAGE):
        time.sleep(2)

    pyautogui.click(CLERIC_EQUIP_COORDS, duration=0.25)
    logging.info('Clicked on Cleric Equipment button.')
    time.sleep(2)

    pyautogui.click(EQUIP_UP_ARROW_COORDS, duration=0.25)
    time.sleep(2)
    pyautogui.click(EQUIP_SLOT_2_COORDS, duration=0.25)     # click "sacred weapon hymmnos"
    time.sleep(2)

    #if pyautogui.locateOnScreen(imgPath("develop_big_ok.png"), region=GAME_REGION):
    pyautogui.click(DEVELOP_BIG_COORDS, duration=0.25)
    time.sleep(2)
    pyautogui.click(DEVELOP_SMALL_COORDS, duration=0.25)
    time.sleep(7)

    while not getGameStatus(CONTINUE_RESEARCH_PAGE):
        time.sleep(5)

    pyautogui.click(CLOSE_COORDS, duration=0.25)
    time.sleep(2)
    pyautogui.click(TOP_LEFT_BUTTON_COORDS, duration=0.25)


def startMainQuests():
    # click on Play
    logging.info('Looking for Play button...')
    while not getGameStatus(PLAY_PAGE):
        pyautogui.click(PLAY_BUTTON_COORDS, duration=0.25)
        time.sleep(2)

    logging.info('Clicked on Play button.')

    pyautogui.click(CHAPTER_ONE_BUTTON_COORDS, duration=0.25)
    logging.info('Clicked on Chapter 1 - Interdimensional Girls.')

    while not getGameStatus(INTERDIMENSIONAL_GIRLS_PAGE):
        time.sleep(2)

    pyautogui.click(SLOT_2_BUTTON_COORDS, duration=0.25)
    logging.info('Clicked on Quest 1 - Spice Run.')

    time.sleep(1)
    pyautogui.click(ACCEPT_QUEST_BUTTON_COORDS, duration=0.25)
    logging.info('Clicked on Accept Quest 1 - Spice Run.')

    time.sleep(2)
    pyautogui.click(PARTY_BEGIN_STORY_COORDS, duration=0.25)
    logging.info('Clicked on Party Accept Quest 1 - Spice Run.')

    time.sleep(2)
    # check if enough food
    if getGameStatus(FOOD_NOT_ENOUGH):
        pyautogui.click(CLOSE_NO_FOOD_BUTTON_COORDS, duration=0.25)
        logging.info('No food. Delay for 30 mins.')
        time.sleep(30*60)   # wait for 30 mins
        logging.info('Wakes up.')
        pyautogui.click(PARTY_BEGIN_STORY_COORDS, duration=0.25)


    time.sleep(5)
    while not getGameStatus(QUEST_ONGOING_PAGE):
        time.sleep(2)
        logging.info('Quest not starting yet.')

    pyautogui.click(FAST_FORWARD_BUTTON_COORDS)
    logging.info('Clicked on Fast Forward button.')    # no way to check if it's actually clicked

    time.sleep(2*60)    # wait 3 mins

    quest_running = True
    while quest_running:
        # random mouse move to prevent screen saver
        #pyautogui.moveTo(random.randint(1, 10), random.randint(1, 10), 2)
        pyautogui.doubleClick(FAST_FORWARD_BUTTON_COORDS)
        time.sleep(10)
        quest_running = getGameStatus(QUEST_ONGOING_PAGE)
        if not quest_running:
            time.sleep(3)
            quest_running = getGameStatus(QUEST_ONGOING_PAGE)   # check again to confirm

    while not getGameStatus(CEO_OFFICE_PAGE):
        pyautogui.click(CENTER_COORDS, duration=0.25)    # continue clicking until back to CEO Office
        logging.info('Clicked to continue.')
        time.sleep(2)


def startHollyQuests():
    # click on Play
    logging.info('Looking for Play button...')
    while not getGameStatus(PLAY_PAGE):
        pyautogui.click(PLAY_BUTTON_COORDS, duration=0.25)
        time.sleep(5)

    logging.info('Clicked on Play button.')


    pyautogui.click(CHAR_STORY_COORDS, duration=0.25)
    logging.info('Clicked on Character Story button.')

    while not getGameStatus(CHAR_STORY_PAGE):
        time.sleep(5)


    pyautogui.click(CHAR_STORY_UP_ARROW_COORDS, duration=0.25)
    logging.info('Clicked on Character Story Up button.')

    #while (getCurrentPage() != CHAR_STORY_PAGE):
    time.sleep(2)
    pyautogui.click(CHAR_STORY_HOLLY_COORDS, duration=0.25)
    logging.info('Clicked on Holly Character Story button.')

    time.sleep(2)
    pyautogui.click(CHAR_STORY_EP1_COORDS, duration=0.25)
    time.sleep(2)
    pyautogui.click(CHAR_STORY_BEGIN_STORY_COORDS, duration=0.25)
    time.sleep(2)
    pyautogui.click(PARTY_BEGIN_STORY_COORDS, duration=0.25)
    logging.info('Begin story...')
    time.sleep(2)


    # check if enough food
    if getGameStatus(FOOD_NOT_ENOUGH):
        pyautogui.click(CLOSE_NO_FOOD_BUTTON_COORDS, duration=0.25)
        logging.info('No food. Delay for 30 mins.')
        time.sleep(30*60)   # wait for 30 mins
        logging.info('Wakes up.')
        pyautogui.click(PARTY_BEGIN_STORY_COORDS, duration=0.25)

    time.sleep(7)
    while not getGameStatus(QUEST_ONGOING_PAGE):
        time.sleep(4)

    pyautogui.click(FAST_FORWARD_BUTTON_COORDS)
    logging.info('Clicked on Fast Forward button.')    # no way to check if it's actually clicked

    time.sleep(4*60)    # wait 4 mins
    pyautogui.doubleClick(FAST_FORWARD_BUTTON_COORDS)   # prevent screen saver from kicking in
    time.sleep(2*60)    # wait 2 mins

    quest_running = True
    while quest_running:
        # random mouse move to prevent screen saver
        #pyautogui.moveTo(random.randint(1, 10), random.randint(1, 10), 2)
        pyautogui.doubleClick(FAST_FORWARD_BUTTON_COORDS)
        time.sleep(10)
        quest_running = getGameStatus(QUEST_ONGOING_PAGE)
        if not quest_running:
            time.sleep(3)
            quest_running = getGameStatus(QUEST_ONGOING_PAGE)   # check again to confirm

    while not getGameStatus(CEO_OFFICE_PAGE):
        pyautogui.click(CENTER_COORDS, duration=0.25)    # continue clicking until back to CEO Office
        logging.info('Clicked to continue.')
        time.sleep(2)

def imgPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often.
       Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)


if __name__ == '__main__':
  main()

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 17-Sep-2016    shianchin    2      Improve locateOnScreen with smaller region.
# 13-Aug-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------
