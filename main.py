import pygame
from pygame import mixer
import random
import math

# Initializes the pygame
pygame.init()

# creates the display size of the game (1200pixels by 800pixels) stores in the variable screen
screen = pygame.display.set_mode((1200, 800))

# Creating a title and icon
pygame.display.set_caption("Space Invaders")  # renames the name of the game
game_Icon = pygame.image.load('Space_Invaders_Icon.png')  # loads the icon
pygame.display.set_icon(game_Icon)  # calls the icon

# Background
background = pygame.image.load("background.png")

# initializes the shooting sound effect
shoot_sound = pygame.mixer.Sound("bullet sound.wav")
shoot_sound.set_volume(0.3) # sets the volume


# creating the start menu
def start():

    # initializes the background music
    mixer.music.load("Intergalactic Odyssey.ogg")
    mixer.music.set_volume(0.08) # sets the volume
    mixer.music.play(-1) # restarts everytime the player goes to the start menu (retries the game)

    on = True
    # global variable for the alien's movement speed
    global alien_speed

    while on:

        # draws the background, coordinates must be 0,0 to cover the whole screen
        screen.blit(background, (0, 0))

        # Renders and displays the text for the rules.
        rules_text1 = pygame.font.Font("freesansbold.ttf", 50).render( # Font styles of the text
            "How To Play:", True, (255, 255, 255)) # RGB value of the text
        screen.blit(rules_text1, (50, 100)) # X and Y positions of the text

        rules_text2 = pygame.font.Font("freesansbold.ttf", 30).render(
            "Arrow Keys to move left and right", True, (255, 255, 255))
        screen.blit(rules_text2, (50, 150))

        rules_text3 = pygame.font.Font("freesansbold.ttf", 30).render(
            "Click spacebar to shoot", True, (255, 255, 255))
        screen.blit(rules_text3, (50, 200))

        rules_text4 = pygame.font.Font("freesansbold.ttf", 30).render(
            "Get 25 points to reach the boss", True, (255, 255, 255))
        screen.blit(rules_text4, (50, 250))

        rules_text5 = pygame.font.Font("freesansbold.ttf", 30).render(
            "Hit the boss 30 times to win", True, (255, 255, 255))
        screen.blit(rules_text5, (50, 300))

        rules_text6 = pygame.font.Font("freesansbold.ttf", 30).render(
            "If enemies reach the bottom of the screen, you lose", True, (255, 255, 255))
        screen.blit(rules_text6, (50, 350))

        difficulty_text = pygame.font.Font("freesansbold.ttf", 35).render(
            "On your keyboard, press e for Easy, m for Medium, or h for Hard", True, (255, 255, 255))
        screen.blit(difficulty_text, (50, 450))

        # This for loop detects if the user presses e,m, or h. These inputs determine the difficulty and the alien movement speed. The higher the difficulty, the greater the speed of the alien
        # Once a valid input is pressed, the main function will begin and the start function will be terminated
        for event in pygame.event.get(): # checks for actions such as keyboard input and mouse clicks
            if event.type == pygame.QUIT:  # if the x on the top right is clicked, close the game window
                pygame.quit()
            if event.type == pygame.KEYDOWN: # if a key is pressed

                if event.key == pygame.K_e: #if that key is e
                    alien_speed = 0.35 # alien speed is 0.35
                    main() # calls the main function
                    on = False

                if event.key == pygame.K_m: #if that key is m
                    alien_speed = 0.5 # alien speed is 0.5
                    main() # calls the main function
                    on = False

                if event.key == pygame.K_h: # if that key is h
                    alien_speed = 0.7 # alien speed is 0.7
                    main() # calls the main function
                    on = False
        # updates the screen (without this, the screen will only appear for one frame and then disappear)
        pygame.display.update()


# function that initializes the main game
def main():
    # Draws the player image on the screen using the x and y coordinates of 568 pixels and 700 pixels
    player_image = pygame.image.load("spaceship.png")
    playerX = 568
    playerY = 700
    playerX_change = 0  # Variable used for the movement speed of the spaceship

    # These global variables are used in other functions
    global bullet_state # states will be defined as either loaded or fire
    global bulletX # X position of the bullet
    global bulletY # Y positon of the bullet
    global bulletX_change # change in the bullet's X position
    global bulletY_change # change in the bullet's Y position
    global font #default font
    global running
    # running is used for the while loop
    running = True

    def player(x, y):
        screen.blit(player_image, (x, y))  # blit draws something on the screen. Uses the image and the image coordinates in the parameters

    # alien
    # lists are needed to draw and define features for more than one alien on the screen while only using one png file of the alien
    alien_image = [] # Draws the alien
    alienX = [] # X position of the alien
    alienY = [] # Y position of the alien
    alienX_change = [] # change in the alien's X position
    alienY_change = [] # change in the alien's Y position
    num_of_aliens = 13

    # this for loop allows for the code to effect all of the aliens by using empty lists and append
    for i in range(num_of_aliens):
        alien_image.append(pygame.image.load("alien.png")) # loads in the image of the alien and appends it to the alien_image list
        alienX.append(random.randint(0, 1050))  # spawns in a random place - X coord
        alienY.append(random.randint(50, 450))  # spawns in a random place - Y coord
        alienX_change.append(alien_speed)  # alienX_change speed is determined by the variable alien_speed
        alienY_change.append(150)  # alien moves downward by 150 pixels

    def alien(x, y, i): # define a function for the aliens
        screen.blit(alien_image[i], (x, y)) # draws the aliens using the for loop conditions above

    # alien boss
    alien_boss_image = pygame.image.load("alien_boss.png")
    alien_bossX = random.randint(0, 1050)  # spawns in a random place - X coord
    alien_bossY = 50  # spawns off screen (boss should not appear during the start of the game)
    alien_bossX_change = 0.6  # Boss moves on the x-axis at a speed of 0.6 pixels per frame
    alien_bossY_change = 200  # When the boss hits an edge, it moves downward by 200 pixels
    boss_HP = 10  # bosses health (must hit 30 times to kill the boss)
    boss_HP_font = pygame.font.Font("freesansbold.ttf", 32)  # initializes the font and text size of the boss' health
    boss_HP_textX = 10  # pixels on the screen where the font will go
    boss_HP_textY = 40  # pixels on the screen where the font will go

    def alien_boss(x, y): # define a function for the alien boss
        # draws the alien boss
        screen.blit(alien_boss_image, (x, y))

    # bullet for ship
    bullet_image = pygame.image.load("bullet.png") # loads in the bullet but does not draw it
    bulletX = 1500  # bullet's x position when the bullet is not being fired (off screen so that the aliens cannot hit it when it is not being shot)
    bulletY = 705  # the y position of the bullet is leveled right below the spaceship
    bulletY_change = 4  # speed of the bullet moving up
    # loaded means we can't see it but we can shoot it
    bullet_state = "loaded"

    # Score value
    score_value = 0
    font = pygame.font.Font("freesansbold.ttf", 32)  # initializes the font and text size
    game_over_font = pygame.font.Font("freesansbold.ttf", 70)  # initializes the font and text size
    textX = 10  # these numbers refer to the pixels - x-coord
    textY = 10  # these numbers refer to the pixels - y-coord

    # function for the score
    def show_score(x, y):
        score = font.render("Score " + str(score_value), True, (
            255, 255, 255))  # renders the font and prints the score, make the font white using RGB values
        screen.blit(score, (x, y))  # draws out the function using blit

    # boss HP
    def show_boss_HP(x, y):
        boss_HP_text = boss_HP_font.render("Boss HP: " + str(boss_HP), True,
                                           (255, 255, 255))  # draws out the number of health points the boss has
        screen.blit(boss_HP_text, (x, y))

    # bullet states
    def bullet(x, y):
        global bullet_state
        bullet_state = "fire" # This state will be used to prevent multiple bullets from being shot before a bullet returns to the player
        screen.blit(bullet_image, (
            x + 16, y - 10))  # bullet is initially drawn from the center and a bit above the spaceship when fired

    # Creating bullet collision using the distance formula (sqrt (x2-x1)^2 + (y2-y1)^2)
    def bullet_collision(alienX, alienY, bulletX, bulletY):
        distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
        if distance < 17:  # bullet is in contact with an alien
            return True
        else:
            return False

    # creating bullet collision for the boss using the distance formula (sqrt (x2-x1)^2 + (y2-y1)^2)
    def shooting_boss_collision(alienX, alienY, bulletX, bulletY):
        distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
        if distance < 70:  # bullet is in contact with the boss
            return True
        else:
            return False

    # game over function
    def game_over():
        # writes down the game over text for losing
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (400, 300))
        try_again_text = game_over_font.render("Press ENTER to try again", True, (255, 255, 255))
        screen.blit(try_again_text, (170, 500))

        # if the "enter" key is pressed, the game will restart (if game over screen is being shown)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start()

    def you_win():
        # writes down the game over text for winning
        game_over_text = game_over_font.render("YOU SAVED THE WORLD!", True, (255, 255, 255))
        screen.blit(game_over_text, (150, 300))
        try_again_text = game_over_font.render("Press ENTER to try again", True, (255, 255, 255))
        screen.blit(try_again_text, (170, 500))

        # if the "enter" key is pressed, the game will restart (if you win screen is being shown)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start()

    # Game Loop
    while running:
        # draws the background, coordinates must be (0,0) to cover the whole screen
        screen.blit(background, (0, 0))
        # in the for loop, it looks for each event that is occurring.
        # an event is any action is the game like mouse movement, keyboard clicks, etc
        for event in pygame.event.get():
            # pygame.QUIT is the close button (x at the top right) If it is pressed, the window closes and the while loop is terminated (running = False)
            if event.type == pygame.QUIT:
                running = False
                # checks if a keystroke is pressed
            if event.type == pygame.KEYDOWN:
                # if the keystroke is the left arrow, move ship left by 0.9 pixels
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.9
                # if the keystroke is the right arrow, move ship right by 0.9 pixels
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.9

                    # calls the bullet function if the space bar is pressed
                if event.key == pygame.K_SPACE:
                    if bullet_state == "loaded":  # without this if statement, the bullet changes position if space is pressed before the bullet is either off screen or in contact with an alien which shouldn't happen
                        bulletX = playerX  # bulletX equals to the spaceship's current X position. Otherwise if the parameter was playerX, the bullet would follow the player's X position after being shot rather than going straight up
                        bullet(bulletX, bulletY)  # calls the bullet function using the bullet's X and Y coordinates
                        shoot_sound.play()  # play the shoot sound effect

            # If an arrow key is released, or if the spaceship has reached the edge of the screen, stop moving the ship
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or player_image == 0 or player_image == 1200:
                    playerX_change = 0

        # players current position is added to the change variable (allows for movement when key is pressed)
        playerX += playerX_change
        # creates a boundary so the spaceship cannot go off the map
        if playerX <= 0:
            playerX = 0
        elif playerX >= 1136:
            playerX = 1136

        # alien movement. The for loop uses lists to refer to each alien
        for i in range(num_of_aliens):
            # Game Over
            if alienY[i] > 700 and score_value < 25:  # if an alien is off screen and the score is lower than 25
                for x in range(num_of_aliens):
                    alienY[x] = 2000  # move all aliens off screen and run the game_over function
                game_over()
                break

            alienX[i] += alienX_change[i]  # movement for the aliens on the x axis (redraws the aliens)
            if alienX[i] <= 8:  # if an alien hits the edge of the screen on the left side
                alienX[i] = 8  # make sure they do not go off screen
                alienY[i] += alienY_change[
                    i]  # alien's current Y position is added to this variable (alien moves down the screen)
                alienX_change[
                    i] = alien_speed  # The change speed is equal to alien_speed (determined through difficulty chosen) and the alien moves towards the right side
            elif alienX[i] >= 1131:  # if an alien reaches the right side of the screen
                alienX[i] = 1131  # make sure they do not go off screen
                alienY[i] += alienY_change[
                    i]  # alien's current Y position is added to this variable (alien moves down the screen)
                alienX_change[i] = -alien_speed  # alien starts moving to the left side (negative of alien speed)

            collision = bullet_collision(alienX[i], alienY[i], bulletX,
                                         bulletY)  # collision is the state of if a bullet collides with an alien using this function. The parameters are the bullet's X and Y coordinates as well as the alien's X and Y coordinates.
            if collision:  # if collision is True
                bulletY = 705  # bullet returns to it's original Y position
                bulletX = 1500 # bullet moves off screen while loaded so that the aliens don't come in contact with the bullet before it is fired
                bullet_state = "loaded"  # bullet returns to ship and is "loaded"
                score_value += 1  # score increases by 1

                # spawns the alien again on a random point on the screen
                alienX[i] = random.randint(0, 1050)
                alienY[i] = random.randint(50, 450)

            # The aliens are continuously being drawn
            alien(alienX[i], alienY[i], i)

        # if statement for the boss and its movement (aliens moving out of the way and boss' own collision hit-box)
        if score_value >= 25:  # if the score is greater than or equal to 25 (May be a time where it exceeds 25 which is why it is greater than or equal to 25)
            show_boss_HP(boss_HP_textX, boss_HP_textY)  # display the bosses health points
            for i in range(num_of_aliens):
                alienY[i] = 2000  # move all aliens off screen

            alien_boss(alien_bossX, alien_bossY)  # display the boss
            alien_bossX += alien_bossX_change  # boss movement on the x axis

            if alien_bossX <= 20:  # if the boss hits the edge of the screen on the left side
                alien_bossX = 20  # make sure it does not go off screen
                alien_bossY += alien_bossY_change  # boss' current Y position is added to this variable (boss moves down the screen)
                alien_bossX_change = 0.6  # Boss' speed is 0.6 pixel towards the right per frame
            elif alien_bossX >= 1100:  # else if the boss hits the edge of the screen on the right side
                alien_bossX = 1100  # make sure it does not go off screen
                alien_bossY += alien_bossY_change  # boss' current Y position is added to this variable (boss moves down the screen)
                alien_bossX_change = -0.6  # Boss' speed is 0.6 pixel towards the left per frame (a negative number is needed to move towards the left)

            collision2 = shooting_boss_collision(alien_bossX, alien_bossY, bulletX,
                                                 bulletY)  # collision2 is the state of if a bullet collides with the boss using this function. The parameters are the bullet's X and Y coordinates as well as the boss' X and Y coordinates.
            if collision2:  # if collision 2 is True
                boss_HP -= 1  # boss loses 1 health point
                bulletY = 705  # bullet returns to it's original Y position
                bullet_state = "loaded"  # bullet is now loaded

            if boss_HP <= 0:  # if the boss has 0 health points left
                you_win()  # initiate the you_win function
                alien_bossY = 2000  # move the boss off screen

            if alien_bossY >= 650 and boss_HP > 0:  # if the boss reaches the bottom of the screen and it has more than 0 health points left
                alien_bossY = 2000  # move the boss off screen
                game_over()  # initiate the game_over function

        # bullet movement
        if bullet_state == "fire":  # when the bullet state is fire
            bullet(bulletX, bulletY) # bullet function is called using the bullet's X and Y coordinates
            bulletY -= bulletY_change #The bullet moves up
            if bulletY <= 0: # if the bullet reaches the top of the screen
                bulletY = 700 # bullet returns to its original position
                bullet_state = "loaded" #bullet is in the loaded state

        # calls the player function and the show_score function
        player(playerX, playerY)
        show_score(textX, textY)

        # update the display (similar to fps)
        pygame.display.update()


# initiate the start function
start()
