import pygame
import sys
import subprocess

pygame.init()

# Set up the screen
screen_width = 650
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Octave Selection")

# Set up fonts
font = pygame.font.Font('assets/Terserah.ttf', 25)

# Define button properties
button_width = 200
button_height = 75
button_color = (100, 100, 100)
button_text_color = (255, 255, 255)
button_font = pygame.font.Font('assets/Terserah.ttf', 30)

# Calculate the x and y coordinates for centering buttons
button_x = (screen_width - button_width) // 2
button_y = ((screen_height - (3 * button_height)) // 3) - 20

# Create buttons with centered positions
buttons = {
    "1_octave": pygame.Rect(button_x, button_y, button_width, button_height),
    "2_octaves": pygame.Rect(button_x, button_y * 2 + button_height, button_width, button_height),
    "3_octaves": pygame.Rect(button_x, button_y * 3 + 2 * button_height, button_width, button_height),
}

def draw_title_bar():
    title_text = font.render('Select the number of octaves you would like to use:', True, 'black')
    
    # Calculate the position to center the title horizontally
    title_x = (screen_width - title_text.get_width()) // 2
    
    screen.blit(title_text, (title_x, 20))
    
    title_text = font.render('Select the number of octaves you would like to use:', True, 'white')
    screen.blit(title_text, (title_x + 2, 22))

run = True
while run == True:
    # Draw background
    screen.fill("teal")
    draw_title_bar()

    # Draw buttons
    for button, rect in buttons.items():
        pygame.draw.rect(screen, button_color, rect) # draws each buttons rectangle
        pygame.draw.rect(screen, (0, 0, 0), rect, 2) # draws a border
        button_text = button_font.render(button.replace("_", " ").title(), True, button_text_color) # takes the name of the button and draws it...
        text_rect = button_text.get_rect(center=rect.center) # In the centre of it's rectangle
        screen.blit(button_text, text_rect) # Displays on screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run == False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button, rect in buttons.items(): # If one of the buttons are clicked...
                if rect.collidepoint(event.pos):
                    # Run the corresponding script based on the button pressed
                    if button == "1_octave":
                        pygame.quit()
                        subprocess.run(["python", "1octave.pyw"], creationflags=subprocess.CREATE_NO_WINDOW)
                        sys.exit()
                    elif button == "2_octaves":
                        pygame.quit()
                        subprocess.run(["python", "2octaves.pyw"], creationflags=subprocess.CREATE_NO_WINDOW)
                        sys.exit()
                    elif button == "3_octaves":
                        pygame.quit()
                        subprocess.run(["python", "3octaves.pyw"], creationflags=subprocess.CREATE_NO_WINDOW) 
                        sys.exit()
                    
                        
        elif event.type == pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    run == False
                    pygame.quit()
                    sys.exit()

    pygame.display.flip()
        
pygame.quit()
sys.exit()