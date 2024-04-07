### INITIALISATION ###

# First Initialise Libraries:

import pygame
import piano_lists as pl
from pygame import mixer
import random
import sys
import subprocess

# Initialise PyGame
pygame.init() # Starts PyGame
pygame.mixer.set_num_channels(10) # The number of sound objects that can be played simulataneously.

# Declares how frequently the screen refreshes:

fps = 60 # 60 refreshes a second
timer = pygame.time.Clock() # knows how long a second is using a clock module which uses real time.

# Declares the game state:

game_state = "playing"  # Possible values: "playing", "results"




### COMMONLY USED GUI DIMENSIONS ###

# Using PyGame's data to store the display dimensions to be used later in the script.

screen_info = pygame.display.Info()
screen_width = screen_info.current_w # For a 1920x1080 monitor will be 1920
screen_height = screen_info.current_h # For a 1920x1080 monitor will be 1080

# Declares the actual dimensions of the window I will be using - not fullscreen.

WIDTH = screen_width - 200 # I want the actual window to be 100 pixels from each side of the screen...
HEIGHT = screen_height - 500 # ...and 250 from the top and bottom of the screen.
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # Declares the surface with the previous dimensions.

# Declare the fonts I'm going to use under different variables for different cirumstances, but ultimately for consistency.

large_font = pygame.font.Font('assets/Terserah.ttf', 48)
medium_font = pygame.font.Font('assets/Terserah.ttf', 28)
small_font = pygame.font.Font('assets/Terserah.ttf', 16)
real_small_font = pygame.font.Font('assets/Terserah.ttf', 10)

# Declares dimensions of a generic button, though I can change the button dimensions of independent buttons if necessary

button_width = 100
button_height = 50
button_color = (100, 100, 100)
button_text_color = (255, 255, 255)
button_font = medium_font

# Declares the dimensions of the rectangles that will be used as buttons:
# [Dimensions have been explained within the Design section of the documentation]
replay_button_rect = pygame.Rect(WIDTH - button_width - 10, 10, button_width, button_height)
submit_button_rect = pygame.Rect(WIDTH // 2 - 50, 170, button_width, button_height)
restart_button_rect = pygame.Rect(WIDTH // 2 - 50, 350, button_width, button_height)
back_button_rect = pygame.Rect(10, 10, 150, button_height)
note_display_rect = pygame.Rect(0, 130, WIDTH, 50)

pygame.display.set_caption("Perfect Pitch App") # Displays 'Perfect Pitch App' at the top of the window's border




### GAMEPLAY LOGIC ###

# Declaring variable and arrays to store the game data:

correct_guesses = []
incorrect_guesses = []
score = 0
notes_guessed = 0
max_notes = 20 # A limit of 20 random notes to guess before displaying results
note_presses = 0 # Initialisation of number of notes pressed per random note guess




### SOUND INITIALISATION ###

# Declares arrays for sounds:

white_sounds = []
black_sounds = []
piano_sounds = []

# Arrays for the notes that have been pressed, so the keys can be dimmed
active_whites = []
active_blacks = []

# Stores the imported arrays of notes:

two_octave = pl.two_octave
two_octavewhites = pl.two_octavewhites
two_octaveblacks = pl.two_octaveblacks

# Appends each note in the given octave to the necessary array.

for i in range(len(two_octavewhites)):
    white_sounds.append(mixer.Sound(f'assets\\notes\\{two_octavewhites[i]}.wav'))

for i in range(len(two_octaveblacks)):
    black_sounds.append(mixer.Sound(f'assets\\notes\\{two_octaveblacks[i]}.wav'))

for i in range(len(two_octave)):
    piano_sounds.append(mixer.Sound(f'assets\\notes\\{two_octave[i]}.wav'))


### GUI DRAWING SUBROUTINES ###


def draw_piano(whites, blacks):
    # Initialize lists to store rectangles for white and black keys
    white_rects = []
    black_rects = []
    
    # Calculate the total width of the piano and its starting position

    piano_width = 14 * 35 # 14 for the 14 white keys and 35 for number of pixels wide each white key is
    piano_x = (WIDTH - piano_width) // 2 # x-position to start drawing the piano
    piano_y = 250  # y-position to start drawing the piano
    
    # Draw white keys
    for i in range(14): # Draws 14 rectangles for the 14 independent white keys in two octaves
        white_rect = pygame.draw.rect(screen, 'white', [piano_x + (i * 35), piano_y, 35, 300], 0, 2)
        white_rects.append(white_rect)
        # Draw black borders for the white keys
        pygame.draw.rect(screen, 'black', [piano_x + (i * 35), piano_y, 35, 300], 2, 2)
        # Render and display key labels for white keys
        key_label = small_font.render(two_octavewhites[i], True, 'black')
        screen.blit(key_label, (piano_x + (i * 35) + 3, piano_y + 280))
         # Draw grey color for pressed white keys
        for i in range(len(whites)):
            if whites[i][1] > 0:
                j = whites[i][0]
                pygame.draw.rect(screen, 'grey', [piano_x + (j * 35), piano_y + 200, 35, 100], 2, 2)
                whites[i][1] -= 1
    
    # Initialize variables for handling black keys positioning
    skip_count = 0
    last_skip = 3
    skip_track = 0
    
    # Draw black keys
    for i in range(10): # 10 for the 10 black keys in two octaves
        # Calculate the position of the black key, considering skips
        black_rect = pygame.draw.rect(screen, 'black', [piano_x + 23 + (i * 35) + (skip_count * 35), piano_y, 24, 200], 0, 2)
        # Check if there are any active black keys
        for q in range(len(blacks)):
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    # Draw grey color border for pressed black keys
                    pygame.draw.rect(screen, 'grey', [piano_x + 23 + (i * 35) + (skip_count * 35), piano_y, 24, 200], 2, 2)
                    blacks[q][1] -= 1
        # Render and display key labels for black keys
        key_label = real_small_font.render(two_octaveblacks[i], True, 'white')
        screen.blit(key_label, (piano_x + 25 + (i * 35) + (skip_count * 35), piano_y + 180))
        black_rects.append(black_rect)
        
        # Handle skips between black keys
        skip_track += 1
        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1
        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1
    
   
    
    # Return the lists of white and black rectangles along with modified lists of whites and blacks
    return white_rects, black_rects, whites, blacks


def draw_title_bar():
    #Render the text
    shadow_text = large_font.render('Perfect Pitch Trainer!', True, 'black')
    title_text = large_font.render('Perfect Pitch Trainer!', True, 'white')
    
    # Calculate the position to center the title horizontally
    title_x = (WIDTH - title_text.get_width()) // 2
    
    # The shadow needs to be drawn first so it is placed behind the title text
    screen.blit(shadow_text, (title_x-2, 28)) # Offset by two pixels either way to get a shadow effect
    screen.blit(title_text, (title_x, 30))  

def draw_replay_button():
    replay_button_rect = pygame.Rect(WIDTH - button_width - 10, 10, button_width, button_height)
    
    # Draw button background
    pygame.draw.rect(screen, button_color, replay_button_rect)
    
    # Draw black border
    pygame.draw.rect(screen, 'black', replay_button_rect, 2)  # The '2' here specifies the border width
    
    # Draw button text
    button_text = button_font.render('Replay', True, button_text_color)

    text_rect = button_text.get_rect(center=replay_button_rect.center) # finds the centre of the retangle to be drawn in
    screen.blit(button_text, text_rect)


def draw_note_display(note):
    # Draw note display box
    pygame.draw.rect(screen, 'white', note_display_rect)
    pygame.draw.rect(screen, 'black', note_display_rect, 2)
    
    # Draw note text
    note_text = medium_font.render(f'Your Guess: {note}', True, (0, 0, 0))
    text_rect = note_text.get_rect(center=note_display_rect.center)
    screen.blit(note_text, text_rect)

def draw_score():
    score_text = small_font.render(f'Score: {score}/{max_notes}', True, 'white')
    screen.blit(score_text, (10, 70))

def draw_feedback():
    feedback_text = small_font.render(f'Correct: {", ".join(correct_guesses)} | Incorrect: {", ".join(incorrect_guesses)}', True, 'white')
    screen.blit(feedback_text, (10, 100))

def draw_submit_button():

    # Draw button background
    pygame.draw.rect(screen, button_color, submit_button_rect)

    # Draw black border
    pygame.draw.rect(screen, (0, 0, 0), submit_button_rect, 2)

    # Draw button text
    button_text = button_font.render('Submit', True, button_text_color)
    text_rect = button_text.get_rect(center=submit_button_rect.center)
    screen.blit(button_text, text_rect)


def display_results():
    screen.fill('teal')  # Clear the screen

    # Calculate a percentage to be displayed
    score_percentage = (score / max_notes) * 100


    result_text = large_font.render(f'Your Score: {score} ({score_percentage}%)', True, 'white')
    screen.blit(result_text, ((WIDTH - result_text.get_width()) // 2, (HEIGHT - result_text.get_height()) // 2))

    # Display correct notes
    correct_notes_text = small_font.render(f'Correct Notes: {", ".join(correct_guesses)}', True, 'white')
    screen.blit(correct_notes_text, ((WIDTH - correct_notes_text.get_width()) // 2, 150))

    # Display incorrect notes
    incorrect_notes_text = small_font.render(f'Incorrect Notes: {", ".join(incorrect_guesses)}', True, 'white')
    screen.blit(incorrect_notes_text, ((WIDTH - incorrect_notes_text.get_width()) // 2, 200))

    # Advice text
    if score_percentage > 75:
        advice_text = small_font.render('You have achieved over 80%. You should try adding another octave!', True, 'white')
        screen.blit(advice_text, ((WIDTH - advice_text.get_width()) // 2, (HEIGHT - advice_text.get_height()) // 2 + 40))
    elif score_percentage < 25:
        advice_text = small_font.render("You seem to be struggling. Practice makes perfect!", True, 'white')
        screen.blit(advice_text, ((WIDTH - advice_text.get_width()) // 2, (HEIGHT - advice_text.get_height()) // 2 + 40))
    else: 
        advice_text = small_font.render("You're doing great! Try again?", True, 'white')
        screen.blit(advice_text, ((WIDTH - advice_text.get_width()) // 2, (HEIGHT - advice_text.get_height()) // 2 + 40))

def draw_restart_button():
    # Draw button background
    pygame.draw.rect(screen, button_color, restart_button_rect)
    
    # Draw black border
    pygame.draw.rect(screen, (0, 0, 0), restart_button_rect, 2)  # The '2' here specifies the border width
    
    # Draw button text
    button_text = button_font.render('Restart', True, button_text_color)
    text_rect = button_text.get_rect(center=restart_button_rect.center)
    screen.blit(button_text, text_rect)

def draw_back_button():
    # Draw button background
    pygame.draw.rect(screen, button_color, back_button_rect)
    
    # Draw black border
    pygame.draw.rect(screen, (0, 0, 0), back_button_rect, 2)  
    
    # Draw button text
    back_button_font = pygame.font.Font('assets/Terserah.ttf', 18)
    button_text = back_button_font.render('Octave Selection', True, button_text_color)
    text_rect = button_text.get_rect(center=back_button_rect.center)
    screen.blit(button_text, text_rect)

def draw_number_of_guesses():
    number_of_guesses_text = small_font.render(f'{3 - note_presses}/3 Guesses Left', True, 'white')
    screen.blit(number_of_guesses_text, (WIDTH - 130, 100))


run = True
note_pressed = ""

randomNum = random.randint(0, len(two_octave) - 1)
pygame.mixer.Sound.play(piano_sounds[randomNum])
randomNote = two_octave[randomNum]

while run:
    timer.tick(fps)
    screen.fill('teal')
    white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)#
    draw_title_bar()#
    draw_replay_button()#
    draw_note_display(note_pressed)#
    draw_submit_button()#
    draw_score()#
    draw_feedback()#
    draw_back_button()#
    draw_number_of_guesses()#


    if game_state == "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                if note_presses < 3:
                    black_key = False
                    for i in range(len(black_keys)):
                        if black_keys[i].collidepoint(event.pos): # If a click is detected on any black key.
                            black_sounds[i].play(0, 1000) # Use the index of the black key to play the corresponding sound
                            black_key = True # a black key has been pressed, so the app will not also play a white key 
                            active_blacks.append([i, 30]) # Display the grey border around the pressed key
                            note_pressed = two_octaveblacks[i] # Stores the name of the key pressed to compare
                            note_presses += 1 # Adds 1 to the number of notes pressed to limit the user to 3

                    for i in range(len(white_keys)):
                        if white_keys[i].collidepoint(event.pos) and not black_key: 
                            # If a click is detected on a white key and doesn't overlap a black key
                            white_sounds[i].play(0, 3000) # Use the index of the white key to play the corresponding sound
                            active_whites.append([i, 30]) # Display the grey border around the pressed key
                            note_pressed = two_octavewhites[i] # Stores the name of the key pressed to compare
                            note_presses += 1 # Adds 1 to the number of notes pressed to limit the user to 3


                if replay_button_rect.collidepoint(event.pos):
                    pygame.mixer.Sound.play(piano_sounds[randomNum])


                if submit_button_rect.collidepoint(event.pos) and note_pressed != '':
                    notes_guessed += 1 # Increment number of total guesses made
                    if note_pressed == randomNote:
                        correct_guesses.append(randomNote)
                        score += 1
                    else:
                        incorrect_guesses.append(randomNote)

                    if notes_guessed == max_notes:
                        # Change the game state to "results"
                        game_state = "results"
                        break
        
                    # Reset the counters for the next guess
                    note_presses = 0

                    # Generates a new random note
                    randomNum = random.randint(0, len(two_octave) - 1)
                    randomNote = two_octave[randomNum]
                    pygame.mixer.Sound.play(piano_sounds[randomNum])

                if back_button_rect.collidepoint(event.pos):
                    run = False  # Set run to False to exit the loop and close the app
                    pygame.quit()
                    subprocess.run(["python", "main.pyw"], creationflags=subprocess.CREATE_NO_WINDOW)
                    

            if event.type == pygame.KEYDOWN:

                if event.key== pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    elif game_state == "results":
        display_results()
        draw_restart_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    # Reset the game state and variables
                    game_state = "playing"
                    score = 0
                    correct_guesses = []
                    incorrect_guesses = []
                    notes_guessed = 0
                    note_presses = 0
                    note_pressed = ""

                    # Generate a new random note
                    randomNum = random.randint(0, len(two_octave) - 1)
                    randomNote = two_octave[randomNum]
                    pygame.mixer.Sound.play(piano_sounds[randomNum])
    if run == True:
        pygame.display.flip()
run = False
pygame.quit()
sys.exit()


