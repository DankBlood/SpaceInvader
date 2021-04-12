def main():
    import pygame
    import random
    import math
    # import time
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

    # Player
    player_image = pygame.image.load("spaceship_no_shoot.png")
    playerX = 568
    playerY = 700
    playerX_change = 0

    global bullet_state
    global bulletX
    global bulletY
    global bulletX_change
    global bulletY_change
    global running
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
        alienX_change.append(0.5)
        alienY_change.append(150)


    def alien(x, y, i):
        screen.blit(alien_image[i], (x, y))


    # alien boss
    alien_boss_image = pygame.image.load("alien_boss.png")
    alien_bossX = random.randint(0, 1050)  # spawns in a random place - X coord
    alien_bossY = 50  # spawns off screen
    alien_bossX_change = 0.6
    alien_bossY_change = 200
    boss_HP = 30
    boss_HP_font = pygame.font.Font("freesansbold.ttf", 32)  # initializes the font and text size
    boss_HP_textX = 10 #pixels on the screen where the font will go
    boss_HP_textY = 40 #pixels on the screen where the font will go
    def alien_boss(x, y):
        screen.blit(alien_boss_image, (x, y))


    # bullet for boss
    # boss_bullet_image = []
    # boss_bulletX = []
    # boss_bulletY = []
    # boss_bulletX_change = []
    # boss_bulletY_change = []
    # num_boss_bullets = 6


    # bullet for ship
    bullet_image = pygame.image.load("bullet.png")
    bulletX = 0
    bulletY = 570
    bulletX_change = 0
    bulletY_change = 4
    # loaded means we can't see it, fire means the bullet is fired/moving
    bullet_state = "loaded"

    # Score
    score_value = 0
    font = pygame.font.Font("freesansbold.ttf", 32)  # initializes the font and text size
    game_over_font = pygame.font.Font("freesansbold.ttf", 70)  # initializes the font and text size
    textX = 10  # these numbers refer to the pixels - x-coord
    textY = 10  # these numbers refer to the pixels - y-coord


    # function for the score
    def show_score(x, y):
        score = font.render("Score " + str(score_value), True, (255, 255, 255))  # renders the font and prints the score, if the score is printed, make the font white using RGB values
        screen.blit(score, (x, y))  # draws out the function using blit

    # boss HP
    def show_boss_HP(x, y):
        boss_HP_text = boss_HP_font.render("Boss HP: " + str(boss_HP), True, (255, 255, 255))
        screen.blit(boss_HP_text, (x, y))

        # bullet states
    def bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bullet_image, (x + 16, y - 10))  # bullet is drawn from the center and a bit above the spaceshi


    # creating bullet collision using the distance formula (sqrt (x2-x1)^2 + (y2-y1)^2
    def bullet_collision(alienX, alienY, bulletX, bulletY):
        distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
        if distance < 27:
            return True
        else:
            return False


    def shooting_boss_collision(alienX, alienY, bulletX, bulletY):
        distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
        if distance < 70:
            return True
        else:
            return False


    # game over function
    def game_over():
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (400, 300))
        try_again_text = game_over_font.render("Press ENTER to try again", True, (255, 255, 255))
        screen.blit(try_again_text, (170, 500))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                main()
        if event.type == pygame.QUIT:
            running = False

    def you_win():
        game_over_text = game_over_font.render("YOU SAVED THE WORLD!", True, (255, 255, 255))
        screen.blit(game_over_text, (150, 300))
        try_again_text = game_over_font.render("Press ENTER to try again", True, (255, 255, 255))
        screen.blit(try_again_text, (170, 500))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                main()
        if event.type == pygame.QUIT:
            running = False

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
                # if the keystroke is left, move ship left by 0.2 pixels
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.8
                # if the keystroke is right, move ship right by 0.2 pixels
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.8

                    # calls the bullet function if the space bar is pressed. BulletX equals to the spaceship's current X
                    # position. After that, the X position of the bullet is whatever bulletX is. Otherwise if the
                    # parameter was playerX, the bullet would follow the player's position after being shot rather than
                    # going straight up

                if event.key == pygame.K_SPACE:
                    # without this if statement, the bullet changes position is space is pressed again
                    if bullet_state == "loaded":
                        bulletX = playerX
                        bullet(bulletX, bulletY)
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
            if alienY[i] > 700 and score_value < 25:
                for x in range(num_of_aliens):
                    alienY[x] = 2000
                game_over()
                break
            alienX[i] += alienX_change[i]
            if alienX[i] <= 0:
                alienX[i] = 0
                alienY[i] += alienY_change[i]
                alienX_change[i] = 0.3
            elif alienX[i] >= 1136:
                alienX[i] = 1136
                alienY[i] += alienY_change[i]
                alienX_change[i] = -0.3
            collision = bullet_collision(alienX[i], alienY[i], bulletX, bulletY)
            if collision:
                # bullet returns to ship and is "loaded"

                bullet_state = "loaded"
                # score increases by 1
                score_value += 1
                print(score_value)
                # spawns the alien again
                alienX[i] = random.randint(0, 1050)
                alienY[i] = random.randint(50, 450)
            alien(alienX[i], alienY[i], i)


    # Giant Statement for the boss and its movement and stuff (aliens moving out of the way  and bosses own collision hit-box)
        if score_value >= 25:
            show_boss_HP(boss_HP_textX, boss_HP_textY)
            for i in range(num_of_aliens):
                alienY[i] = 2000

            alien_boss(alien_bossX, alien_bossY)
            alien_bossX += alien_bossX_change

            if alien_bossX <= 20:
                alien_bossX = 20
                alien_bossY += alien_bossY_change
                alien_bossX_change = 0.6
            elif alien_bossX >= 1100:
                alien_bossX = 1100
                alien_bossY += alien_bossY_change
                alien_bossX_change = -0.6

            collision2 = shooting_boss_collision(alien_bossX, alien_bossY, bulletX, bulletY)
            if collision2:
                boss_HP -= 1
                bulletY = 700
                bullet_state = "loaded"

            if boss_HP <= 0:
                you_win()
                alien_bossY = 2000

            if alien_bossY >= 650 and boss_HP > 0:
                alien_bossY = 2000
                game_over()


    # bullet movement
        if bullet_state == "fire":  # when the bullet state is fire, the function is called, the bullet moves up and when the bullet reaches the top of the screen, the bullet returns
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
main()