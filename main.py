# ------------------------------------------------------------------------------------------------
# BUGS/things to edit/things to consider: 
# 1) code cleanliness (test lines, commenting format, redundencies, difficult to understand
#    variables,etc ...)
#  General Note: want to be addictive (think flow), not too boring and not too difficult
# 2) Incorportate Lab Streaming Layer functionality
# 3) for LSL... when you do win.flip() make sure to tie push to that
# def flip(event_name):
# win.callonflip(outlet, .... [event])
# win.flip
# fix off by one error
# Note: MAKE EVERYTHING EASY TO CHANGE LATER
# ------------------------------------------------------------------------------------------------
#import psychopy
#from egi_pynetstation import NetStation
import asyncio
import pygame as pg
import sys
from random import choice, uniform,randint
import os
#from scipy.special import comb
#from scipy.stats import norm
from math import sqrt, floor, factorial, erfc, exp, log, pi
#import messagescreens
from datetime import *
import time
from csv import reader
from numpy import nanmean, nanstd
from warnings import filterwarnings
import math

#import pylsl

print("in main after imports")

print("here at MOT_constants")
test2 = 'messagescreens!'
print(f'in MOT_constants. {test2=}')
pg.init()

# == Path For Storing Trial Results. ==
save_path = 'C:\\Users\\Administrator\\psychexperiment\\multiple-object-tracking-paradigm\\results\\'
"""
Define the object class attributes
"""
obj_radius: int = 35  # size of balls in pixels

"""
Define the times and durations in SECONDS
"""
fix_draw_time = Tfix = 1.5 # time to present fixation cross and objects

flash_time = Tfl = fix_draw_time + 1  # time for targets to flash

animation_time = Tani = flash_time + 4.5  # time for objects to move around in seconds

answer_time = Tans = animation_time + 60  # time limit to make answer

feedback_time = 1

info = pg.display.Info()
win_width = info.current_w
win_height = info.current_h
win_dimension = (win_width, win_height)

"""
Define the project display window
"""
title = "Multiple Object Tracking Experiment"

"""# getting window size (will handle dpi later)
winfo = [] #stores monitor info as a string so we can extract window size info
for m in get_monitors():
    winfo.append(m)

win_width = m.width
win_height = m.height  # pixels; width of screen
win_dimension = (win_width, win_height)
"""



"""
Define instruction texts.
"""
def start_text(num_targ, total):
    return "You will first see a cross at the center of the screen. Please focus your gaze to that cross.\n\n" \
    "There will be " + str(total) + " circles appearing on the screen, " + str(num_targ) + " of them will flash in GREEN.\n" \
    "The cross will disappear, and all circles will start to move. Keep track of those " + str(num_targ) + \
    " flashed circles.\n\nWhen the circles stop moving, select which circles you've been tracking by clicking " \
    "them.\nWhen you have made your selection, press the SPACEBAR to submit your selection.\n\n" \
    "Press F to start when you are ready.\n\nIf you need to stop, let the experimenter know or press ESCAPE if you are in the middle of a trial. "\

def start_text_nback():
    return "Welcome to the n-back task. \n\n" \
    "In this experiment you will see a sequence of letters.\n\n" \
    "Your goal is to remember these letters and identify when a letter repeats itself after n number of letters. For example, if n = 1, then" \
    " you are performing a 1-back task and you must remember when the same letter occurs twice in a row. For a 2-back you must identify" \
    " when a pattern repeats with some other pattern in between. If 'X','Y','Z' are three letters, then a 1-back is a sequence such as '...X,X...'"\
    ", a 2-back is a sequence such as '...X, Y, X...' and a 3-back would be '...X, Y, Z, X...' .\n\n" \
    "Press the SPACEBAR when you see one of these \'n-back\' targets.\n" \
    "Remember: In a 1-back task, you only click the spacebar for 1-backs, in a 2-back you only click the spacebar for 2-backs,... \n\n"\
    "Press F to start when you are ready.\n\nIf you need to stop, let the experimenter know or press ESCAPE if you are in the middle of a trial. "\
    "Furthermore, you may press \"k\" to skip through the practice trials once the balls have been displayed."
    

fix_text = "First, you will see this cross. Please focus your gaze here. \nPress F to continue."

practice_text = "You will now practice with a 1-back task and a 2-back task. \n\nPress F to continue."
def input_text():
    return "Please enter the requested information. Then press Enter or Return to continue. Press ESC to exit or inform the observer of your decision. \n\n"

def present_text(num_targ, total): 
    return "Now, " + str(total) + " circles will appear randomly around the screen. " + str(num_targ) + " random " \
    "circles will flash briefly. Remember which circles flashed. The cross will disappear, and all circles " \
    "will start moving when the flashing stops.\n\nPress F to continue."\
    

submit_ans_txt = "When the circles stop moving, select the circles that you've been tracking.\n" \
                 "You will have {:d} seconds to make your choice.\n\n" \
                 "Press SPACEBAR to submit your answer.".format(int(answer_time-animation_time))

prac_finished_txt = "The practice is now over.\n\nPress the F when you are ready to continue to the real " \
                    "experiment.\nRemember to keep track of the targets and submit your result by " \
                    "pressing the SPACEBAR.\n\nBe as quick and accurate as you can!\n\n" \
                    "Press F to continue."

experim_fin_txt = "The experiment is now over; let the experimenter know.\n\nThank you for participating!" \
                  "\n\nPress F to exit."

guide_fin_txt = "The guide is now complete, and you will move to practice rounds, where you will go through the " \
                "experiment in normal order, but your answers will not be recorded.\n\nAfter the practice is finished, " \
                "you will move to the real experiments where your responses will be recorded.\n\n" \
                "Press F to move to the practice rounds."

guide_fin_txt_nback = "The guide is now complete.\n\n" \
                "Press F to move to the real rounds."

guide_submit_txt = "You've selected {:d} targets correctly."

guide_timeup_txt = "Time is up! You will now repeat the trial."

def high_scores_info_txt(high_scores):
    return "Current High Scores \n\n 1. " + str(high_scores[0]) + "\n\n 2. " + str(high_scores[1]) + "\n\n 3. " \
         + str(high_scores[2]) + "\n\n 4. " + str(high_scores[3]) + "\n\n 5. " + str(high_scores[4])


def stage_txt(game):
        return " Stage " + str(game["stage"]) 

# == Font size ==
extra_large_font = 120
large_font = 72
med_font = 42
small_font = 12

"""
Define some colours.
"""
# == Greyscale ==
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [128, 128, 128]
SLATEGREY = [112, 128, 144]
DARKSLATEGREY = [47, 79, 79]
default_color = WHITE
# == Yellows ==
YELLOW = [255, 255, 0]
OLIVE = [128,128,0]
DARKKHAKI = [189,183,107]

# == Greens ==
GREEN = [0, 128, 0]
GREENYELLOW = [173, 255, 47]

RED = [255, 50, 50]

"""
Generate random x and y coordinates within the window boundary
"""
boundary_size: int = 30 # how large the boundary is

def make_boundary(win_height, win_width):
    boundary_location = ['up', 'down', 'left', 'right']
    boundary_coord = [obj_radius + boundary_size, (win_height - (obj_radius + boundary_size)), obj_radius + boundary_size, (win_width - (obj_radius + boundary_size))]
    boundary = dict(zip(boundary_location, boundary_coord))
    listX, listY = [], []
    rangeX, rangeY = range(boundary['left'], boundary['right']), range(boundary['up'], boundary['down'])
    return boundary

boundary = make_boundary(win_height, win_width)

"""
Define session information for recording purposes
"""
session_info = {'Observer': 'Type observer initials', 'Participant': 'Type participant ID'}
date_string = time.strftime("%b_%d_%H%M", time.localtime())  # add the current time


def brownian_motion(C1, C2):
    """ ===== FUNCTION TO CALCULATE BROWNIAN MOTION ===== """
    c1_spd = math.sqrt((C1.dx ** 2) + (C1.dy ** 2))
    diff_x = -(C1.x - C2.x)
    diff_y = -(C1.y - C2.y)
    vel_x = 0
    vel_y = 0
    if diff_x > 0:
        if diff_y > 0:
            angle = math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
        elif diff_y < 0:
            angle = math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
    elif diff_x < 0:
        if diff_y > 0:
            angle = 180 + math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
        elif diff_y < 0:
            angle = -180 + math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
    elif diff_x == 0:
        if diff_y > 0:
            angle = -90
        else:
            angle = 90
        vel_x = c1_spd * math.cos(math.radians(angle))
        vel_y = c1_spd * math.sin(math.radians(angle))
    elif diff_y == 0:
        if diff_x < 0:
            angle = 0
        else:
            angle = 180
        vel_x = c1_spd * math.cos(math.radians(angle))
        vel_y = c1_spd * math.sin(math.radians(angle))
    if vel_x == 0 and vel_y == 0:
        vel_x, vel_y = 1.5, 1.5
    C1.dx = vel_x
    C1.dy = vel_y

#print (win_dimension)

test = 5
print(f'in messagescreens. {test=}')

# == Set window ==
x, y = 50, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
# = visual.window.Window(size=win_dimension, fullscr=True, winType='pygame')
win = pg.display.set_mode(win_dimension, pg.FULLSCREEN)
pg.display.set_caption(title)

# == Define colors. ==
background_col = GREY
hover_col = DARKSLATEGREY
click_col = GREENYELLOW
select_col = YELLOW

# Lab Streaming Layer push (pushes a string to the outlet)
#def LSL_push(outlet, string):
#    pylsl.StreamOutlet.push_sample(outlet, [string])

def draw_boundaries(display=win):
    #pg.draw.rect(display, BLACK, pg.Rect(win_width - boundary_size, 0, boundary_size, win_height - boundary_size)) # right
    pg.draw.rect(display, BLACK, pg.Rect(win_width - boundary_size, 0, boundary_size, win_height)) # right
    pg.draw.rect(display, BLACK, pg.Rect(0, 0, boundary_size, win_height)) # left
    pg.draw.rect(display, BLACK, pg.Rect(0, 0, win_width, boundary_size)) # top
    pg.draw.rect(display, BLACK, pg.Rect(0, win_height - boundary_size, win_width, boundary_size)) # bottom
    #pg.display.update()

def wait_key():
    """function to wait key press"""
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                return

def draw_square(outlet, tag, mlist, display=win):
        # -- Function to draw circle onto display
        #outlet.send_event(event_type = tag)
        pg.draw.rect(display, WHITE, pg.Rect(0, win_height - 20, 20,20))
        if tag == 'CLCK' or tag == 'UCLK' or tag == 'SPCE':
            static_draw(mlist)
        #pg.draw.rect(display, BLACK, pg.Rect(21, win_height - 20, win_width - 21,20))
        if tag == 'FLSH' or (tag[0] == 'F' and tag[1] == 'X'):
            pg.display.flip()
        else:    
            pg.display.update([pg.Rect(0, win_height - 20, 20,20), None])
        return pg.time.get_ticks()

def draw_square2(display=win):
        # -- Function to draw circle onto display
        pg.draw.rect(display, WHITE, pg.Rect(0, win_height - 20, 20,20))



def flash_targets(dlist, tlist, flash, gametype, outlet, flash_start_record):
    """function to flash targets"""
    play_sound = False
    fixation_cross()
    if flash == True:
        play_sound = True
        for t in tlist:
            t.color = GREEN
            t.draw_circle(win)
            flash = False
        if gametype == 'real':
            #draw_square(outlet, 'FLS', 0)
            pass
    else:
        for t in tlist:
            t.color = default_color
            t.draw_circle(win)
    for d in dlist:
        d.draw_circle(win)
    if flash_start_record == False and gametype == 'real': # record start of flash screen
        #LSL_push(outlet, 'FLSH0') # flash start
        draw_square(outlet, 'FLS', 0)
        flash_start_record = True
    #else:
    #    if pg.time.get_ticks() - start_time < 200 and flash == False:
    #        draw_square2()
    pg.display.flip()
    return flash, flash_start_record

def animate(dlist, tlist, mlist, gametype, outlet, mvmt_start):
    """function to move or animate objects on screen"""
    for m in mlist:
        m.detect_collision(mlist)
        m.draw_circle(win)
        if gametype == 'real' and mvmt_start == False:
            draw_square(outlet, 'MVE0', 0)
            #LSL_push(outlet, 'MVE') #start move
            mvmt_start = True
    pg.display.flip()
    return mvmt_start

def static_draw(mlist):
    """function for static object draw"""
    for obj in mlist:
        obj.draw_circle()

def fixation_cross(color=BLACK):
    """function to draw fixation cross"""
    start_x, end_x = ((win_width/2)-7, (win_height/2)) , ((win_width/2)+7, (win_height/2))
    start_y, end_y = (win_width/2, (win_height/2)-7), (win_width/2, (win_height/2)+7)
    pg.draw.line(win, color, start_x, end_x, 3)
    pg.draw.line(win, color, start_y, end_y, 3)

def fixation_screen(mlist, gametype, outlet, fix_record, stage):
    """function to present the fixation cross and the objects"""
    fixation_cross(BLACK)
    for obj in mlist:
        obj.draw_circle()
    if gametype == 'real' and fix_record == False: # record start of fixation screen
        level = stage + 1 # given the math, the level the user is on is the stage plus one
        fixation_tag = 'FX' + str(level) # add the level to the end of the string
        if len(fixation_tag) < 4: # if single digit, then add a trailing X
            fixation_tag = fixation_tag + 'X'
        draw_square(outlet, fixation_tag, 0)
        fix_record = True
        #LSL_push(outlet, 'FIX0') #fixation start
    pg.display.flip()
    return fix_record

def text_objects(text, color, textsize):
    """text object defining text"""
    msg = pg.font.SysFont("arial", textsize)
    text_surf = msg.render(text, True, color)
    return text_surf, text_surf.get_rect()  # - Returns the text surface and rect object

def msg_to_screen(text, textcolor, textsize, pos, display=win):
    """function to render message to screen centered"""
    text_surface, text_rect = text_objects(text, textcolor, textsize)  # - set variable for text rect object
    text_rect.center = pos
    draw_boundaries()
    display.blit(text_surface, text_rect)
    pg.display.flip()

def msg_to_screen_centered(text, textcolor, textsize, display=win):
    """function to render message to screen centered"""
    too_big = True
    text_x = 0
    max_w = win_width-(win_width/10)
    #while too_big == True:
    text_surface, text_rect = text_objects(text, textcolor, textsize)  # - set variable for text rect object
    text_rect.center = (win_width/2), (win_height/2)
    draw_boundaries()
    display.blit(text_surface, text_rect)
    pg.display.flip()
        #if text_x <= max_w:
         #   too_big = False

def multi_line_message(text, textsize, pos=((win_width-(win_width/10)), win_height), color=BLACK, display=win):
    """function to split text message to multiple lines and blit to display window."""
    # -- Make a list of strings split by the "\n", and each list contains words of that line as elements.
    #font = pg.font.SysFont("arial", textsize)
    #words = [word.split(" ") for word in text.splitlines()]
    too_big = True 
    final_text_x = 0

    # -- Get the width required to render an empty space
    #space_w = font.size(" ")[0]  # .size method returns dimension in width and height. [0] gets the width
    #max_w, max_h = ((win_width-(win_width/10)), win_height)
    #text_x, text_y = pos

    while too_big == True:
        font = pg.font.SysFont("arial", textsize)
        words = [word.split(" ") for word in text.splitlines()]
        space_w = font.size(" ")[0]  # .size method returns dimension in width and height. [0] gets the width
        max_w, max_h = ((win_width-(win_width/10)), win_height)
        text_x, text_y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)  # get surface for each word
                word_w, word_h = word_surface.get_size()  # get size for each word
                if text_x + word_w >= max_w:  # if the a word exceeds the line length limit
                    text_x = (win_width/10)  # reset the x
                    text_y += word_h  # start a new row
                display.blit(word_surface, (text_x, text_y))  # blit the text onto surface according to pos
                text_x += word_w + space_w  # force a space between each word
            final_text_x = text_x
            text_x = (win_width/10)  # reset the x
            text_y += word_h  # start a new row
        if text_y <= win_height - boundary_size - 20:
            too_big = False
        else: 
            textsize -= 3 # if too big for display then shrink the textsize and try again
            win.fill(background_col)
        draw_boundaries()
    pg.display.flip()

def message_screen(message, num_targ, total, display=win):
    if message == "start":
        display.fill(background_col)
        multi_line_message(start_text(num_targ, total), med_font, ((win_width - (win_width / 10)), 120))
    if message == "not_selected_enough":
        multi_line_message("Select " + str(num_targ) + " circles!", med_font, (win_width/2, win_height/2))
    if message == "timeup":
        display.fill(background_col)
        msg_to_screen_centered("Time's up! Now resetting", BLACK, large_font)
        pg.display.flip()
    if message == "prac_finished":
        display.fill(background_col)
        multi_line_message(prac_finished_txt, med_font, ((win_width - (win_width / 10)), 120))
        pg.display.flip()
    if message == "exp_finished":
        display.fill(background_col)
        multi_line_message(experim_fin_txt, large_font, ((win_width - (win_width / 10)), 150))
        pg.display.flip()

def stage_screen(stage):
    win.fill(background_col)
    msg_to_screen_centered("Level " + str(stage), BLACK, large_font)
    pg.display.flip()
    pg.time.delay(1500)

def correct_txt(selected, total, audio_path):
    win.fill(background_col)
    if selected == total:
        msg_to_screen_centered("Good! " + str(selected) +  " out of " + str(total) + " correct", BLACK, large_font)
    else:
        msg_to_screen_centered("Sorry... " + str(selected) +  " out of " + str(total) + " correct", BLACK, large_font)
    pg.display.flip()
                    # plays sounds
    if selected == total:
        pg.mixer.music.load(os.path.join(audio_path,'correct.ogg'))
    else:
        pg.mixer.music.load(os.path.join(audio_path,'incorrect.ogg'))
    pg.mixer.music.set_volume(0.22)
    pg.mixer.music.play()
    pg.time.delay(2000)
    pg.mixer.music.unload()

def guide_screen(call, mlist, selected_targets_list, num_targ, total):
    if call == "start":
        win.fill(background_col)
        multi_line_message(start_text(num_targ, total), med_font, ((win_width - (win_width / 10)), 120))
        pg.display.flip()
    if call == "focus":
        win.fill(background_col)
        fixation_cross()
        multi_line_message(fix_text, med_font, ((win_width - (win_width / 10)), (win_height / 2 + 30)))
        pg.display.flip()
    if call == "present":
        win.fill(background_col)
        fixation_cross()
        static_draw(mlist)
        multi_line_message(present_text(num_targ, total), med_font, ((win_width - (win_width / 10)), (win_height / 2 + 30)))
        pg.display.flip()
    if call == "answer":
        static_draw(mlist)
        multi_line_message(submit_ans_txt, med_font, ((win_width - (win_width / 10)), (win_height / 2 + 30)))
        pg.display.flip()
    if call == "timeup":
        win.fill(background_col)
        multi_line_message(guide_timeup_txt, med_font, ((win_width - (win_width / 10)), (win_height / 2 + 30)))
        pg.display.flip()
    if call == "submitted":
        win.fill(background_col)
        msg_to_screen_centered(guide_submit_txt.format(len(selected_targets_list)), BLACK, large_font)
        pg.display.flip()
    if call == "finished":
        win.fill(background_col)
        multi_line_message(guide_fin_txt, med_font,((win_width - (win_width / 10)), 120))
        pg.display.flip()

def user_break_screen():
    win.fill(background_col)
    msg_to_screen_centered("You've Earned a Break!... Press F to continue", BLACK, large_font)
    pg.display.flip()
    wait_key()

def score_screen(score):
    win.fill(background_col)
    msg_to_screen_centered("Score: " + str(score), BLACK, large_font)
    pg.display.flip()
    pg.time.delay(1500)

def is_valid(num):
    if (num >= 48 and num <= 57) or (num >= 97 and num <= 122) or (num == 46) or (num == 32):
        return True
    else:
        return False

def user_info(type):
    pg.mouse.set_visible(False)
    pg.display.flip()
    name = "" # prepping variables
    exit = False

    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    exit_key = event.key
                    exit = True
                elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                    name = name[:-1] #delete last letter
                elif is_valid(event.key):
                    if (pg.key.get_mods() & pg.KMOD_CAPS) or (pg.key.get_mods() & pg.KMOD_SHIFT):
                        name = name + chr(event.key).upper()
                    else:
                        name = name + chr(event.key)
        if exit == True:
            break
        win.fill(background_col) #display input
        multi_line_message(input_text() + type + name, large_font, ((win_width - (win_width / 10)), 120))

    if exit_key == pg.K_RETURN or exit_key == pg.K_KP_ENTER:
        return name # If the user enters then we proceed with game
    else: # otherwise we quit the game
        pg.quit()
        sys.exit()

def play_again_exp():
    response = user_info("Play again? (type \'y\' for yes or \'n\' for no): ")
    while True:
        if response.lower() == 'y':
            return True
        if response.lower() == 'n':
            return False
        response = user_info("Play again? (type \'y\' for yes or \'n\' for no): ")

def high_score_info(high_scores):
    win.fill(background_col)
    multi_line_message(high_scores_info_txt(high_scores), large_font, ((win_width - (win_width / 10)), 40))
    pg.display.flip()
    pg.time.delay(5 * 1000)

def new_high_score(score, i):
    win.fill(background_col)
    msg_to_screen_centered("New High Score! You are now #" + str(i) + "! Your score: " + str(score), GREEN, med_font + 10)
    pg.display.flip()
    pg.time.delay(5 * 1000)

def final_score(score):
    win.fill(background_col)
    msg_to_screen_centered("Your Final score: " + str(score), BLACK, large_font)
    pg.display.flip()
    pg.time.delay(5 * 1000)

def mot_screen():
    win.fill(background_col)
    msg_to_screen_centered("Motion Object Tracking (press F to continue)", BLACK, large_font)
    pg.display.flip()
    wait_key()

# deprecated... turns out that we do not need it
def consent_screens():
    page = 1
    consented = False
    proceed = False
    while consented == False:
        win.fill(background_col)
        for event in pg.event.get():
            if proceed == True:
                if event.key == pg.K_RIGHT:
                    page = page + 1
            if event.key == pg.K_LEFT:
                page = page - 1
        if page <= 1:
            page = 1
            multi_line_message("This is a consent form message", large_font, ((win_width - (win_width / 10)), 40))
        elif page == 2:
            multi_line_message("General info/Purpose text", large_font, ((win_width - (win_width / 10)), 40))
        elif page == 3:
            multi_line_message("Procedures and time required", large_font, ((win_width - (win_width / 10)), 40))
        elif page == 4:
            multi_line_message("Additional procedures info", large_font, ((win_width - (win_width / 10)), 40))
        elif page == 5:
            multi_line_message("Financial info", large_font, ((win_width - (win_width / 10)), 40))
        elif page == 6:
            multi_line_message("Risks and Benefits", large_font, ((win_width - (win_width / 10)), 40))
        elif page == 7:
            multi_line_message("Confidentiality", large_font, ((win_width - (win_width / 10)), 40))
        elif page == 8:
            multi_line_message("Contacts & questions", large_font, ((win_width - (win_width / 10)), 40))
        else:
            page = 9
            multi_line_message("Consent", large_font, ((win_width - (win_width / 10)), 40))
        pg.mouse.set_visible(False)
        pg.display.flip()

#=======================================================================================
#=======================================================================================
#================================ NBACK MESSAGE SCREENS ================================
#=======================================================================================
#=======================================================================================

def guide_screen_nback(call):
    if call == "start":
        win.fill(background_col)
        multi_line_message(start_text_nback(), med_font, ((win_width - (win_width / 10)), 40))
        pg.display.flip()
    if call == "practice":
        win.fill(background_col)
        multi_line_message(practice_text, large_font,((win_width - (win_width / 10)), 120))
        pg.display.flip()
    if call == "finished":
        win.fill(background_col)
        multi_line_message(guide_fin_txt_nback, large_font,((win_width - (win_width / 10)), 120))
        pg.display.flip()
    
def correct_screen(n, correct, fa, total):
    n = str(n)
    win.fill(background_col)
    msg_to_screen_centered(str(correct) +  " out of " + str(total) + " " + "targets identified with " + str(fa) + " mis-clicks.", BLACK, large_font)
    pg.display.flip()
    pg.time.delay((feedback_time + 2) * 1000)

def n_back_screen(n):
    n = str(n)
    win.fill(background_col)
    msg_to_screen_centered("This is a " + n + "-back task.", BLACK, large_font)
    pg.display.flip()
    pg.time.delay((feedback_time + 1) * 1000)

def blank_screen():
    win.fill(background_col)
    pg.display.flip()
    pg.time.delay(2 * 1000)

def nback_screen():
    win.fill(background_col)
    msg_to_screen_centered("N-back Experiment (press F to continue)", BLACK, large_font)
    pg.display.flip()
    wait_key()

print('imported!')
#filterwarnings("ignore") #ignore warnings

# == Game Structure Variables ==
# == Attributes and relations between those attributes ==
attributes = ["targs", "speed", "dists"]
att_max = [3,3] 
scale = 1
dist_range = att_max[1] // 2
starting_targs = 2

# == how far player progresses or regresses based on performance ==
success = 1
failure = -3

# == Trial variables ==
real_time = 12 * (10 ** 5) # time that real trials last (milliseconds)
prac_trials = 2 # number of practice trials
guide_trials = 1 # number of guide trials

# == Processing power or frames per second ==
FPS = 144

# == Defines the Objects (Balls) and their Properties ==
class MOTobj:
    def __init__(self, game, default_color):
        # -- Radius of the circle objects
        self.radius = obj_radius

        # -- Object positions attributes
        info = pg.display.Info()
        win_width = info.current_w
        win_height = info.current_h
        boundary = make_boundary(win_height, win_width)
        self.x, self.y = choice([n for n in range(int(boundary["left"]), int(boundary["right"]))
                                 if n not in range(x - self.radius, x + self.radius)]), \
                        choice([n for n in range(int(boundary["up"]), int(boundary["down"]))
                                 if n not in range(y - self.radius, y + self.radius)])

        # -- Velocity initialization
        self.dx, self.dy = velocity(game)

        # -- Set the circle object neutral state color
        self.color = default_color
        self.default_color = default_color

        # -- Timer attributes
        self.timer = 0
        self.flash = True

        # -- State attributes for mouse selection control
        self.state = ""
        self.isClicked = False
        self.isSelected = False
    
    def change_color(self, color):
        self.color = color

    def in_circle(self, mouse_x, mouse_y):
        # -- Return boolean value deping on mouse position, if it is in circle or not
        if sqrt(((mouse_x - self.x) ** 2) + ((mouse_y - self.y) ** 2)) < self.radius:
            return True
        else:
            return False

    def state_control(self, state):
        # -- Neutral or default state with no form of mouse selection
        if state == "neutral":
            self.color = self.default_color
            self.state = "neutral"
            self.isClicked = self.isSelected = False
        # -- Hovered state if mouse is hovering over circle object
        if state == "hovered":
            self.color = hover_col
            self.state = "hovered"
            self.isClicked = self.isSelected = False
        # -- Clicked state if mouse click DOWN while in object
        if state == "clicked":
            self.color = click_col
            self.state = "clicked"
            self.isClicked = True
            self.isSelected = False
        # -- Selected state if mouse click UP on a "clicked" object
        if state == "selected":
            self.color = select_col
            self.state = "selected"
            self.isClicked = False
            self.isSelected = True

    def draw_circle(self, display=win):
        # -- Function to draw circle onto display
        pg.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)
        
    # add a fix for when dx/dy equals 0 (probably in brownian motion)
    def detect_collision(self, mlist):
        # -- Object positions in x and y coordinates change in velocity value
        self.x += self.dx
        self.y += self.dy
        # -- If the object reaches the window boundary, bounce back
        #boundary = make_boundary(win_height, win_width)
        if self.x < boundary["left"] or self.x > boundary["right"]:
            self.dx *= -1
        if self.y < boundary["up"] or self.y > boundary["down"]:
            self.dy *= -1
        # -- If the object bounces off each other, run the Brownian motion physics
        # objects need to be from the same list, otherwise the objects
        # can pass through each other if they're from a different list
        for a in mlist:
            for b in mlist:
                if a != b:
                    if sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2)) <= (a.radius + b.radius):
                        brownian_motion(a, b)

    def flash_color(self, issquare):
        # -- Function to flash color
        if self.timer == FPS:
            self.timer = 0
            self.flash = not self.flash

        self.timer += 3

        if self.flash:
            self.color = self.default_color
        else:
            if issquare:
                self.color = GREY
            else:
                self.color = GREEN

# randomly shuffles positions of balls
def shuffle_positions(mlist):
    """Shuffle the position of circles"""
    for self in mlist:
        self.x = choice([n for n in range(int(boundary["left"] + 21), int(boundary["right"] - 21))
                         if n not in range(x - self.radius, x + self.radius)])
        self.y = choice([n for n in range(int(boundary["up"] + 21), int(boundary["down"] - 21))
                         if n not in range(y - self.radius, y + self.radius)])


# checks that balls do not spawn in corner or overlap, fixes problem if it occurs
def valid_positions(mlist):
    truth_list = []
    valid_positions = False 
    while (valid_positions == False):
        for m in mlist: # iterate over all balls 
            # check if within boundaries
            if (m.x > boundary["right"]) or (m.x < boundary["left"]) or (m.y > boundary["down"]) or (m.y < boundary["up"]):
                truth_list.append(0) # if located in corner with square then invalid
            for k in mlist:
                distance = sqrt(((m.x - k.x) ** 2) + ((m.y - k.y) ** 2))
                if distance < 2 * m.radius and distance != 0:
                    truth_list.append(0) # if overlapping with another ball then invalid
        if truth_list == []: # if every ball satisfies our condition then we are fine 
            valid_positions = True
        else: #otherwise we shuffle the balls and start again
            shuffle_positions(mlist)
        truth_list = []
    
# get initial dx and dy values for balls
def velocity(game):
    speed = game["speed"]
    overall_velocity = sqrt(2 * ((speed + 2.75) ** 2))
    dx = choice([-1,1]) * uniform(0, overall_velocity)
    dy = choice([-1,1]) * sqrt((overall_velocity ** 2) - (dx ** 2))
    return dx, dy

# == returns product over elements up to and including entry n == 
def product(list, n):
    prod = 1
    for i in range(n):
        if list[len(list)- i - 1] != 0:
            prod *= list[len(list)- i - 1]
    return prod

# == Function for updating a game based on the stage ==
# -- Defines a dictionary called "game"
def update_game(stage):
    if stage < 0:
        stage = 0
    game = {"stage": stage}
    i = 0
    for att in attributes:
        prod = product(att_max, len(att_max) - i)
        if i == len(att_max):
            game[att] = stage
        elif stage >= prod:
            game[att] = stage // prod
            stage -= game[att] * prod
        else:
            game[att] = 0
        i += 1
    game["targs"] += starting_targs
    game["dists"] = game["targs"] - scale * (dist_range - game["dists"])
    if game["dists"] == 0:
        game["dists"] += 1
    return game

# == Generates a List of Objects (Balls) ==
def generate_list(game, color):
    """function to generate new list of objects"""
    target_list = []
    num_targ = game["targs"]
    for nt in range(num_targ):
        t = MOTobj(game, color)
        target_list.append(t)

    distractor_list = []
    num_dist = game["dists"] 
    for nd in range(num_dist):
        d = MOTobj(game, color)
        distractor_list.append(d)
    mlist = distractor_list + target_list # NEW NEw NEW 
    valid_positions(mlist) # NEW NEW NEW after balls for trial generated we make sure they occupy valid positions 
    return distractor_list, target_list

# == Helper Function for Delaying Game by t seconds ==
def delay(t):
    """function to stop all processes for a time"""
    pg.time.delay((t*1000))  # multiply by a thousand because the delay function takes milliseconds

# == Function for Recording User Performance ==
def record_response(participant_number, user_number, name, response_time, targs_identified, game, time_out_state, d_prime, total_time, log):
    # record the responses
    header_list = [participant_number, user_number, name, response_time, targs_identified, game["targs"], game["stage"] + 1, time_out_state, d_prime, total_time]
    # convert to string
    header_str = map(str, header_list)
    # convert to a single line, separated by commas    
    header_line = ','.join(header_str)
    header_line += '\n'
    log.write(header_line)

# == plays proper welcome messages based on gametype ==
def welcome_messages(game, gametype, high_score):
    num_targs = game["targs"]
    num_dists = game["dists"]
    total = num_targs + num_dists
    
    if gametype == 'guide':
        guide_screen("start", [], [], num_targs, total)
        wait_key()

        # == Fixation cross screen ==
        guide_screen("focus", [], [], num_targs, total)
        wait_key()

        # == Present cross and circles screen ==
        guide_screen("present", [], [], num_targs, total)
        wait_key()
    if gametype == 'real':
        #high_score_info(high_score)
        stage_screen(game["stage"] + 1)

# == plays proper end messages based on gametype ==
def end_messages(game, gametype, recorder):
    num_targs = game["targs"]
    num_dists = game["dists"]
    total = num_dists + num_targs
    win.fill(background_col)
    if gametype == 'real':
        message_screen("exp_finished", num_targs, total)
        pg.display.flip()
        wait_key()
        recorder.close()
    elif gametype == 'practice':
        message_screen("prac_finished", num_targs, total)
        pg.display.flip()
        wait_key()
    else:
        guide_screen("finished", [], [], num_targs, total)
        wait_key()

# == determines whether a user can take a break == 
def take_a_break(gametype, total_time):
    if gametype == 'real' and total_time >= (6 * (10 ** 5)):
        return True
    return False

# == updates the score given current score and consecutive correct trials
def update_score(score, consecutive, stage):
    return score + consecutive + floor(stage / 2)

# == function for calculating expected balls correct on a trial if user were guessing
def expected_value(game):
    targs = game["targs"]
    total = targs + game["dists"]
    EV = 0
    for i in range(targs + 1):
        numerator = factorial(targs) // (math.factorial(i) * math.factorial(targs - i))
        denominator = math.factorial(total) // (math.factorial(targs) * math.factorial(total - targs))
        EV += i * (numerator / denominator)
    """for i in range(targs + 1):
        numerator = comb(targs, i) * comb(total - targs, targs - i)
        denominator = comb(total, targs) #combinatorial calculation
        EV += i * (numerator / denominator)"""
    return EV

# == calculates d-prime value ==
def d_prime(dprimes, hit_rate, game):
    total_targs = game["targs"]
    total_balls = game["targs"] + game["dists"]

    hits = round(hit_rate[-1] * total_targs) # calculate targets correctly identified
    misses = total_targs - hits # total misses (which in MOT is equivalent to false alarms)
    farate = misses / (total_balls - total_targs)
    correct_rejections = (total_balls - total_targs) - misses # number of correct rejections

    # values for fixing extreme d primes
    half_hit = 0.5 / (hits + misses)
    half_fa = 0.5 / (misses + correct_rejections)
    # fix extreme hit rate
    hitrate = hit_rate[-1]
    if hitrate == 1:
        hitrate = 1 - half_hit
    if hitrate == 0:
        hitrate = half_hit

    # fix extreme fa rate
    if farate == 1:
        farate = 1 - half_fa
    if farate == 0:
        farate = half_fa

    def erfcinv_approx(x):
        # Check for special cases
        if x == 0:
            return float('inf')
        if x == 2:
            return float('-inf')

        # Approximation of erfcinv using Newton's method
        def f(x, y):
            return erfc(x) - y

        def df(x):
            return -2 / sqrt(pi) * exp(-x**2)

        max_iterations = 100
        tolerance = 1e-10

        # Initial guess
        guess = -log(0.5 * (2 - x))

        # Newton's method iteration
        for _ in range(max_iterations):
            y = f(guess, x)
            if abs(y) < tolerance:
                return guess
            derivative = df(guess)
            if derivative == 0:
                break
            guess -= y / derivative

        # Return the best approximation found
        return guess

    # calculate z values
    z_hit = -sqrt(2) * erfcinv_approx(2 * hitrate)
    z_fa = -sqrt(2) * erfcinv_approx(2 * farate)
    """z_hit = norm.ppf(hitrate)
    z_fa = norm.ppf(farate)"""

    dp = z_hit - z_fa # calculate d prime
    dprimes.append(dp) # add to list
    return dprimes

def update_stage(selected_targ, game, gametype, score, consecutive):
    if len(selected_targ) == game["targs"]:
        game["stage"] += success
        consecutive += 1
        score = update_score(score, consecutive, game["stage"])
    else:
        game["stage"] += failure
        consecutive = floor(consecutive / 2)
        if game["stage"] < 0:
            game["stage"] = 0
    if gametype == 'real': 
        score_screen(score) # display score
    return game, score, consecutive

# == prepares where we store data such as results and high scores ==
def prepare_files():
    participant_number = 1
    high_score = [0] * 5 # get top 5 high scores
    date_sys = str(date.today())
    user_number = user_info("User Number: ")
    name = user_info("Full Name (Please enter your name exactly [e.g. 'John Doe']): ").lower()
    return "log", "highscore_path", high_score, user_number, name, date_sys, "mot/Sound/", participant_number, "results_path"

    """if getattr(sys, 'frozen', False): 
        # The application is frozen (is an executable)
        file_path = os.path.dirname(sys.executable)
    else:
        # The application is not frozen (is not an executable)
        file_path = os.path.dirname(__file__)
    
    MOT_etc_path = os.path.join(file_path, "MOT_etc")
    try: # create a folder for results and highscores if none exists
        os.mkdir(MOT_etc_path)
    except:
        pass
    results_path = os.path.join(MOT_etc_path, "Results_MOT_exp")

    try:
        os.mkdir(results_path)
    except: # if folder for results exists then do nothing, otherwise create such a folder
        pass
    
    highscore_path = os.path.join(MOT_etc_path, "Highscore_MOT_exp")
    try:
        os.mkdir(highscore_path) 
    except: # if it does exist, then grab the high score
        with open(os.path.join(highscore_path,'highscores.csv')) as f:
            i = 0
            for line in f: # grabs top 5 high scores 
                if i == 0:
                    pass
                else:
                    if int(line) > high_score[4]:
                        high_score.append(int(line))
                        high_score.sort(reverse=True) 
                i += 1
            f.close()
    else: # if no directory exists then create one and a highscore file
        f = open(os.path.join(highscore_path,'highscores.csv'), 'w')
        f.write('High Scores\n')
        f.close()
        f = open(os.path.join(highscore_path,'highscores.csv'), 'a')
        f.write("0\n")
        f.close()

    # Creating one big csv file for all user data
    results_csv_path = os.path.join(results_path, 'results.csv')
    if not (os.path.isfile(results_csv_path)): # if it doesn't exist, then create a file
        log = open(results_csv_path, 'w')
        header = ["participant number", " user number (for Lauren)", " name", " response_time"," targets_identified"," total_targets"," level"," timed_out"," d_prime", " total_time"]
        delim = ",".join(header)
        delim += "\n"
        log.write(delim)
    else: # if exists, then get new participant number
        log = open(results_csv_path, 'r') 
        i = 0
        for row in reader(log): # grabs last participant number (last line, first entry)
            if i == 0:
                pass
            else:
                participant_number = int(row[0])
            i += 1
        participant_number += 1 # get the very next participant number
    log.close()
    log = open(results_csv_path, 'a')
    audio_path = os.path.join(file_path, 'Sound')
    return log, highscore_path, high_score, user_number, name, date_sys, audio_path, participant_number, results_path"""

# == Runs Real Trials (same as practice but user performance is saved) ==
def trials(game, recorder, gametype, time_or_trials, high_score, audio_path, participant_number, user_number, name, outlet):
    #outlet.resync()
    # == Messages to user based on gametype ==
    welcome_messages(game, gametype, high_score)

    # == Generates the game ==
    dt = 0
    hit_rates = []
    dprimes = []
    list_d, list_t = generate_list(game, WHITE)
    list_m = list_d + list_t
    count = 0
    break_given = False
    flash = True
    reset = False
    submitted = False
    highest_level = 0
    insufficient_selections = False # whole lot of initiating variables in this area
    timeup = False
    score = consecutive = 0 # initializes score and consecutive correct trials
    t0 = start_time = pg.time.get_ticks()
    total_time = 0
    square_time = 0

    #keeps track of which time signatures we have recorded already for a given round
    fix_record = False
    flash_record = False
    mvmt_start = False
    mvmt_stop = False


    # == Controls the "game" part of the game ==
    while True:
        
        num_targs = game["targs"]
        pg.time.Clock().tick_busy_loop(FPS)  # = Set FPS
        win.fill(background_col)  # - fill background with background color
        draw_boundaries()
        mx, my = pg.mouse.get_pos()  # - get x and y coord of mouse cursor on window

        selected_list = []  # - list for all selected objects
        selected_targ = []  # - list for all SELECTED TARGETS

        # == Controls responses to user input ===
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #if gametype == 'real':
                square_time = draw_square(outlet, 'STOP', list_m)
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_k and (gametype == 'guide' or gametype == 'practice'):
                    #LSL_push(outlet,'SKP') #skip
                    #square_time = draw_square(outlet, 'SKP', list_m)
                    return 'k'
                if event.key == pg.K_ESCAPE: # what is going on here
                    square_time = draw_square(outlet, 'ESCP', list_m)
                    if gametype == 'real':
                        #LSL_push(outlet, 'ESC') #escape/quit
                        #square_time = draw_square(outlet, 'ESCP', list_m)
                        return score, dprimes, (game["stage"] + 1), highest_level 
                    else:
                        return 'esc'
                if event.key == pg.K_SPACE and (Tani + 2 < dt <= Tans+ 2):
                    #if gametype == 'real':    
                    #LSL_push(outlet, 'SPC') #space
                    square_time = draw_square(outlet, 'SPCE', list_m)
                    if not reset:
                        for target in list_t:
                            if target.isSelected and not target.isClicked:
                                selected_targ.append(target)
                                selected_list.append(target)
                        for distractor in list_d:
                            if distractor.isSelected and not distractor.isClicked:
                                selected_list.append(distractor)
                        if len(selected_list) == num_targs:
                            submitted = True
                            t_keypress = pg.time.get_ticks()
                        else:
                            insufficient_selections = True
                            insuf_sel_time = pg.time.get_ticks()
            for obj in list_m:
                if obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("hovered")
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if not obj.isClicked and not obj.isSelected:
                            #if gametype == 'real':   
                            square_time = draw_square(outlet, 'CLCK', list_m)
                            #LSL_push(outlet, 'CLK') #click object 
                            obj.state_control("clicked")
                        if not obj.isClicked and obj.isSelected:
                            #if gametype == 'real': 
                            square_time = draw_square(outlet, 'UCLK', list_m)
                            #LSL_push(outlet, 'UCLK') #unclick object 
                            obj.state_control("neutral")
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("selected")
                elif not obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")

        # == Grabs the time after each frame and total time passed in the trial ==
        t1 = pg.time.get_ticks()
        dt = (t1 - t0)/1000

        if count < time_or_trials: # need to edit because we are using time for real trials
            while (pg.time.get_ticks() - square_time < 100):
                draw_square2()
            if not reset:
                #draw_boundaries()
                if dt <= Tfix + 1:
                    if dt < (Tfix + 1) / 4:# and gametype == 'real':
                        draw_square2()
                    for targ in list_m: # hovering does not change color
                        targ.state_control("neutral")
                    pg.mouse.set_visible(False)
                    fix_record = fixation_screen(list_m, gametype, outlet, fix_record, game["stage"])
                elif Tfix + 1 < dt <= Tfl + 1.85:
                    for targ in list_m: # hovering does not change color
                        targ.state_control("neutral")
                    if flash == True:
                        flash, flash_record = flash_targets(list_d, list_t, flash, gametype, outlet, flash_record) # flash color
                        dt = Tfl + 1.95
                        flash = False
                elif Tfl + 1.85 < dt <= Tfl + 2:
                    for targ in list_m: # hovering does not change color
                        targ.state_control("neutral")
                    flash_targets(list_d, list_t, flash, gametype, outlet, flash_record) # reset color
                elif Tfl + 2 < dt <= Tani + 2:
                    if dt < Tfl + 2.1:# and gametype == 'real':
                        draw_square2()
                    pushed_flash_already = False
                    for targ in list_m: # hovering does not change color
                        targ.state_control("neutral")
                    mvmt_start = animate(list_d, list_t, list_m, gametype, outlet, mvmt_start)
                elif Tani + 2 < dt <= Tans+ 2:
                    if mvmt_stop == False:# and gametype == 'real':
                        square_time = draw_square(outlet, 'MVE1', list_m)
                        mvmt_stop = True
                    if Tani + 2 < dt <= Tani + 2.05: # reset mouse position
                        info = pg.display.Info()
                        win_width = info.current_w
                        win_height = info.current_h
                        pg.mouse.set_pos([win_width/2,win_height/2])
                    pg.mouse.set_visible(True)
                    if insufficient_selections:
                        static_draw(list_m)
                        message_screen("not_selected_enough", num_targs, num_targs + game["dists"])
                        static_draw(list_m)
                        if pg.time.get_ticks() - insuf_sel_time > 500:
                            insufficient_selections = False
                    if gametype == 'guide':
                        guide_screen("answer",list_m, selected_targ, num_targs, num_targs + game["dists"]) 
                    else: 
                        static_draw(list_m)
                    pg.display.flip()
                elif Tans + 2 < dt:
                    pg.mouse.set_visible(False)
                    timeup = True

            if submitted: # -- if the user submits answers properly
                total_time = pg.time.get_ticks() - start_time # total time in milliseconds since real trials began
                # == message screen stating performance on that trial ==
                pg.mouse.set_visible(False)
                correct_txt(len(selected_targ), len(list_t), audio_path)
                pg.mouse.set_visible(False)

                                # == Records info for the trial ==
                #if gametype == 'real':
                if len(selected_list) == len(selected_targ):# and gametype == 'real':
                    square_time = draw_square(outlet, 'CRCT', list_m)
                else:
                    #if gametype == 'real':
                    miss_tag = 'MS' + str(len(selected_targ)) + str(num_targs)
                    square_time = draw_square(outlet, miss_tag, list_m)
                hit_rates.append(len(selected_targ) / len(selected_list))
                dprimes = d_prime(dprimes, hit_rates, game)
                d_prime_string = str(dprimes[-1])[:4]
                while len(d_prime_string) < 4:
                    d_prime_string = d_prime_string + '0'
                #outlet.send_event(event_type = d_prime_string)
                t_sub = ((t_keypress - t0)/1000) - animation_time
                record_response(participant_number, user_number, name, t_sub, len(selected_targ), game, False, dprimes[-1], total_time / 1000, recorder)

                # == Based on that performance, we update the stage and score ==
                game, score, consecutive = update_stage(selected_targ, game, gametype, score, consecutive)
                if game["stage"] + 1 > highest_level:
                    highest_level = game["stage"] + 1
                reset = True

            if timeup: # -- if the user runs out of time
                #outlet.send_event(event_type = "TMUP")
                total_time = pg.time.get_ticks() - start_time # total time in milliseconds
                pg.mouse.set_visible(False)
                if gametype == 'real':
                    record_response(participant_number, user_number, name, "timed out", "NA", game, True, "NA", total_time / 1000, recorder)
                message_screen("timeup", num_targs, num_targs + game["dists"])
                delay(feedback_time)
                count -= 1
                reset = True

            if reset: # -- prepare for the next trial
                #if gametype == 'real':
                #outlet.resync() #resynchronize the clock
                #if inter_round_record == False and gametype == 'real':
                #    square_time = draw_square(outlet, 'SCR0')
                    #LSL_push(outlet, 'SCR0') #screens start showing
                #    inter_round_record = True
                pg.mouse.set_visible(False)
                # gives user break after certain amount of time
                if take_a_break(gametype, total_time) and break_given == False:
                    break_given = True
                    user_break_screen()  

                game = update_game(game["stage"])
                list_d, list_t = generate_list(game, WHITE)
                list_m = list_d + list_t
                if gametype != 'real':
                    count += 1
                else:
                    count = total_time #* 1000
                flash = True
                submitted = timeup = insufficient_selections= reset = sound_played = False
                if gametype == 'real':
                    stage_screen(game["stage"] + 1)
                t0 = pg.time.get_ticks()
                
                # resets time signature variables for next round
                fix_record = False
                flash_record = False
                mvmt_start = False
                mvmt_stop = False
                
        else: # -- end of experiment/practice/guide
            #if gametype == 'real':
            square_time = draw_square(outlet, 'STOP', list_m)
                #LSL_push(outlet, 'END')
            pg.mouse.set_visible(False)
            end_messages(game, gametype, recorder)
            if gametype == 'real':
                recorder.close()
                return score, dprimes, (game["stage"] + 1), highest_level
            else:
                return "complete" # signifies succesful completion of prac/guide trials
        

        # total gameplay time (for use in giving users a break)
        total_time = pg.time.get_ticks() - start_time # current time minus the time at which we started 

# == Main Loop.  ==
async def main(unified):
    mot_play_again = True
    while mot_play_again == True:
        # == Initiate pygame and collect user information ==
        #consent_screens()
        #pg.init()
        print("initted!")
        pg.mixer.init()
        log, highscore_path, high_score, user_number, name, date_sys, audio_path, participant_number, results_path = prepare_files()
        

        # prepare lab streaming layer functionality
        #info = pylsl.StreamInfo('MOT_stream', 'Markers', 1, 0, 'string', '_ptcpt_' + str(participant_number) + '_' + date_sys)
        #outlet = pylsl.StreamOutlet(info)

        #prepare netstation functionality 
        #IP address of NetStation - CHANGE THIS TO MATCH THE IP ADDRESS OF YOUR NETSTATION
        IP_ns = '10.10.10.42' #needs to be specified for the computer

        #IP address of amplifier (if using 300
        #series, this is the same as the IP address of
        #NetStation. If using newer series, the amplifier
        #has its own IP address)
        IP_amp = '10.10.10.51'

        #Port configured for ECI in NetStation - CHANGE THIS IF NEEDED
        port_ns = 55513

        #Start recording and send trigger to show this
        #outlet = NetStation.NetStation(IP_ns, port_ns)
        #outlet.connect(ntp_ip = IP_amp)
        #outlet.begin_rec()
        #outlet.send_event(event_type = 'STRT', start = 0.0)
        outlet = 0
        game_guide = update_game(0)
        game_prac = update_game(0)
        game_real = update_game(0)
    
        # == Start guide ==
        key = trials(game_guide, log, 'guide', guide_trials, high_score, audio_path, participant_number, user_number, name, outlet)

        # == Start practice ==
        if key == 'k' or key == 'complete':
            key = trials(game_prac, log, 'practice', prac_trials, high_score, audio_path, participant_number, user_number, name, outlet)

        # == Start real trials, recording responses ==
        if key == 'k' or key == 'complete':
            #outlet.resync()
            square_time = draw_square(outlet, 'STRT', 0)
            while pg.time.get_ticks() - square_time < 100:
                draw_square2()
            #LSL_push(outlet, 'real_trials_start')
            score, dprimes, last_level, highest_level = trials(game_real, log, 'real', real_time, high_score, audio_path, participant_number, user_number, name, outlet)
        else:
            score = 0
    
        if score > high_score[4]: # update high score if applicable  
            i = 4
            while (score > high_score[i]) and (i >= 0): # calculate where on the highscore list it goes
                i = i - 1
            i += 2 # do this because we index from zero

            f = open(os.path.join(highscore_path,'highscores.csv'), 'a')
            f.writelines(str(score) + '\n')
            f.close()
            #new_high_score(score, i)
        else:
            pass
            #final_score(score)

        summary_csv_path = os.path.join(results_path, 'summary.csv')
        if not (os.path.isfile(summary_csv_path)): # if it doesn't exist, then create a file
            f = open(summary_csv_path, 'w')
            header = ["participant number", " user_number (for Lauren)", " name", " dprime_avg", " dprime_std", " highest_level_obtained", " last_level", " score"]
            delim = ",".join(header)
            delim += "\n"
            f.write(delim)
            f.close()
        f = open(summary_csv_path, 'a')
            # record the responses
        try:
            header_list = [participant_number, user_number, name, nanmean(dprimes), nanstd(dprimes), highest_level, last_level, score]
        except:
            header_list = [participant_number, user_number, name, "NaN", "NaN", "NaN", "NaN", "NaN"]
        # convert to string
        header_str = map(str, header_list)
        # convert to a single line, separated by commas    
        header_line = ','.join(header_str)
        header_line += '\n'
        f.write(header_line)
        f.close()

        # allow user to play again without rerunning program
        pg.mixer.quit()
        mot_play_again = play_again_exp()
        if mot_play_again == True:
            if unified == True:
                return True
        else:
            if unified == True:
                return False
            else:
                pg.quit()
                sys.exit()

        await asyncio.sleep(0)

asyncio.run( main(False) )

"""if __name__ == "__main__":
    main(False)"""