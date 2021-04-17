import pygame
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


# creating the start menu
def start():
    on = True
    # global variable for the alien's movement speed
    global alien_speed

    while on:
        # draws in a background
        screen.fill((52, 1, 59))
        # draws the background, coordinates must be 0,0 to cover the whole screen
        screen.blit(background, (0, 0))
        # Text for rules

        rules_text1 = pygame.font.Font("freesansbold.ttf", 50).render(
            "How To Play:", True, (255, 255, 255))
        screen.blit(rules_text1, (50, 100))

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
        # Once a valid input is pressed, the main function will begin
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if the x on the top right is clicked, close the app
                pygame.quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_e:
                    alien_speed = 0.35
                    main()
                    on = False

                if event.key == pygame.K_m:
                    alien_speed = 0.5
                    main()
                    on = False

                if event.key == pygame.K_h:
                    alien_speed = 0.7
                    main()
                    on = False
        # updates the screen (without this, the screen will only appear for one frame and then disappear)
        pygame.display.update()


# function that initializes the main game
def main():
    # Draws the player image on the screen using the x and y coordinates of 568 pixels and 700 pixels
    player_image = pygame.image.load("spaceship_no_shoot.png")
    playerX = 568
    playerY = 700
    playerX_change = 0  # Variable used for the movement speed of the spaceship

    # These global variables are used in other functions
    global bullet_state
    global bulletX
    global bulletY
    global bulletX_change
    global bulletY_change
    global running
    global font
    running = True

    def player(x, y):
        screen.blit(player_image, (x, y))  # blit draws something on the screen, uses the image and the image
        # coordinates in the parameters

    # alien
    alien_image = []
    alienX = []
    alienY = []
    alienX_change = []
    alienY_change = []
    num_of_aliens = 13
    # this for loop applies this code to each alien by using empty lists and append
    for i in range(num_of_aliens):
        alien_image.append(pygame.image.load("alien.png"))
        alienX.append(random.randint(0, 1050))  # spawns in a random place - X coord
        alienY.append(random.randint(50, 450))  # spawns in a random place - Y coord
        alienX_change.append(alien_speed)  # alienX_change speed is determined by the variable alien_speed
        alienY_change.append(150)  # alien moves downward by 150 pixels

    def alien(x, y, i):
        screen.blit(alien_image[i], (x, y))

    # alien boss
    alien_boss_image = pygame.image.load("alien_boss.png")
    alien_bossX = random.randint(0, 1050)  # spawns in a random place - X coord
    alien_bossY = 50  # spawns off screen (boss should not appear during the start of the game)
    alien_bossX_change = 0.6  # Boss moves on the x-axis at a speed of 0.6 pixels per frame
    alien_bossY_change = 200  # When the boss hits an edge, it moves downward by 200 pixels
    boss_HP = 30  # bosses health (must hit 30 times to kill the boss)
    boss_HP_font = pygame.font.Font("freesansbold.ttf", 32)  # initializes the font and text size
    boss_HP_textX = 10  # pixels on the screen where the font will go
    boss_HP_textY = 40  # pixels on the screen where the font will go

    def alien_boss(x, y):
        # draws the alien boss
        screen.blit(alien_boss_image, (x, y))

    # bullet for ship
    bullet_image = pygame.image.load("bullet.png")
    bulletX = 0  # bullet's x position when the bullet is not being fired (off screen so that the aliens cannot hit it)
    bulletY = 570  # the y position of the bullet is leveled right below the spaceship
    bulletY_change = 4  # speed of the bullet moving up
    # loaded means we can't see it, fire means the bullet is fired/moving
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
        bullet_state = "fire"
        screen.blit(bullet_image, (
        x + 16, y - 10))  # bullet is initially drawn from the center and a bit above the spaceship when fired

    # creating bullet collision using the distance formula (sqrt (x2-x1)^2 + (y2-y1)^2)
    def bullet_collision(alienX, alienY, bulletX, bulletY):
        distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
        if distance < 18:  # bullet is in contact with the alien
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

        # if the "enter" key is pressed, the game will restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start()

    def you_win():
        # writes down the game over text for winning
        game_over_text = game_over_font.render("YOU SAVED THE WORLD!", True, (255, 255, 255))
        screen.blit(game_over_text, (150, 300))
        try_again_text = game_over_font.render("Press ENTER to try again", True, (255, 255, 255))
        screen.blit(try_again_text, (170, 500))

        # if the "enter" key is pressed, the game will restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start()

    # Game Loop
    while running:
        # Uses RGB to create the background colour of the game
        screen.fill((52, 1, 59))
        # draws the background, coordinates must be 0,0 to cover the whole screen
        screen.blit(background, (0, 0))
        # in the for loop, it looks for each event that is occurring.
        # an event is any action is the game like mouse movement, keyboard clicks, etc
        for event in pygame.event.get():
            # pygame.QUIT is the close button (x at the top right) If it is pressed, the window closes (running = False)
            if event.type == pygame.QUIT:
                running = False
                # checks if a keystroke is pressed
            if event.type == pygame.KEYDOWN:
                # if the keystroke is left, move ship left by 0.9 pixels
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.9
                # if the keystroke is right, move ship right by 0.9 pixels
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.9

                    # calls the bullet function if the space bar is pressed
                if event.key == pygame.K_SPACE:
                    if bullet_state == "loaded":  # without this if statement, the bullet changes position is space is pressed before the bullet is either off screen or in contact with an alien
                        bulletX = playerX  # BulletX equals to the spaceship's current X position.
                        bullet(bulletX,
                               bulletY)  # Otherwise if the parameter was playerX, the bullet would follow the player's position after being shot rather than going straight up

            # If the key is released, stop moving the ship
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

        # alien movement. The for loop uses  to refer to each alien
        for i in range(num_of_aliens):
            # Game Over
            if alienY[i] > 700 and score_value < 25:  # if an alien is off screen and the score is not 25
                for x in range(num_of_aliens):
                    alienY[x] = 2000  # move all aliens off screen and run the game_over function
                game_over()
                break  # allows for the user to break the while loop if the x on the top-right of the screen is pressed (close the game)

            alienX[i] += alienX_change[i]  # movement for the aliens on the x axis (redraws the aliens)
            if alienX[i] <= 5:  # if an alien hit the edge of the screen on the left side
                alienX[i] = 5  # make sure they do not go off screen
                alienY[i] += alienY_change[
                    i]  # alien's current Y position is added to this variable (alien moves down the screen)
                alienX_change[
                    i] = alien_speed  # The change speed is equal to alien_speed (determined through difficulty chosen)
            elif alienX[i] >= 1131:  # if an alien reaches the right side of the screen
                alienX[i] = 1131  # make sure they do not go off screen
                alienY[i] += alienY_change[
                    i]  # alien's current Y position is added to this variable (alien moves down the screen)
                alienX_change[i] = -alien_speed  # alien starts moving to the left side (negative of alien speed)

            collision = bullet_collision(alienX[i], alienY[i], bulletX,
                                         bulletY)  # collision is the state of if a bullet collides with an alien using this function (defined above)
            if collision:  # if collision is true
                bulletY = 700 # bullet returns to it's original Y position
                bullet_state = "loaded"  # bullet returns to ship and is "loaded
                score_value += 1  # score increases by 1

                # spawns the alien again on a random point on the screen
                alienX[i] = random.randint(0, 1050)
                alienY[i] = random.randint(50, 450)
            alien(alienX[i], alienY[i], i)

        # Giant if statement for the boss and its movement (aliens moving out of the way and bosses own collision hit-box)
        if score_value >= 25:  # if the score is greater than or equal to 25 (May be a time it exceeds 25 which is why it is greater than or equal to 25)
            show_boss_HP(boss_HP_textX, boss_HP_textY)  # display the bosses health points
            for i in range(num_of_aliens):
                alienY[i] = 2000  # move all aliens off screen

            alien_boss(alien_bossX, alien_bossY)  # display the boss
            alien_bossX += alien_bossX_change  # boss movement on the x axis

            if alien_bossX <= 20:  # if the boss hits the edge of the screen on the left side
                alien_bossX = 20  # make sure it does not go off screen
                alien_bossY += alien_bossY_change  # boss' current Y position is added to this variable (boss moves down the screen)
                alien_bossX_change = 0.6  # Boss' speed is 0.6 pixel towards the right per frame
            elif alien_bossX >= 1100:  # if the boss hits the edge of the screen on the right side
                alien_bossX = 1100  # make sure it does not go off screen
                alien_bossY += alien_bossY_change  # boss' current Y position is added to this variable (boss moves down the screen)
                alien_bossX_change = -0.6  ## Boss' speed is 0.6 pixel towards the left per frame (a negative number is needed to move towards the left)

            collision2 = shooting_boss_collision(alien_bossX, alien_bossY, bulletX,
                                                 bulletY)  # collision2 is the state of if a bullet collides with the boss using this function (defined above)
            if collision2:  # if collision 2 is true
                boss_HP -= 1  # boss loses 1 health point
                bulletY = 700  # bullet returns to it's original Y position
                bullet_state = "loaded"  # bullet is now loaded

            if boss_HP <= 0:  # if the boss has 0 health points left
                you_win()  # initiate the you_win function
                alien_bossY = 2000  # move the boss off screen

            if alien_bossY >= 650 and boss_HP > 0:  # if the boss reaches the bottom of the screen and it has more than 0 health points left
                alien_bossY = 2000  # move the boss off screen
                game_over()  # initiate the game_over function

        # bullet movement
        if bullet_state == "fire":  # when the bullet state is fire, the bullet function is called, the bullet moves up and when the bullet reaches the top of the screen, the bullet returns
            # to the loaded state and returns back to the spaceship
            bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = 700
                bullet_state = "loaded"

        # calls the player function and the show_score function
        player(playerX, playerY)
        show_score(textX, textY)

        # update the display (similar to fps)
        pygame.display.update()


# initiate the start function
start()
