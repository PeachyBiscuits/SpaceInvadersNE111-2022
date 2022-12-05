#Title: Face Invaders
#Authors: Ethan, Star, Ryan, Kodey (add lastnames)
#Description: Player controls a ship (movement with leftand right arrow keys and shoot with the space bar)
#             Shoot the aliens before they reach you, level based difficulty will increase with level as well as
#             the score multiplier

import pygame
import math
import random

# initialize pygame
pygame.init()

#create the "game board"
board_width = 1250
board_height = 840

# colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

board = pygame.display.set_mode((board_width, board_height))
pygame.display.set_caption("Face Invaders - NE111")

# fonts to be used
font = pygame.font.SysFont('None', 20)
fail_font = pygame.font.SysFont('None', 70)

# global variable to stroe if a bullet is currently fired 
firing = False

# global variable for the number of aliens at the beginning, will increment for every level 1-5
starting_aliens = 0

# global variable for number of current aliens, initialized at 0
num_aliens = 0

# global variable for alien offsets
alien_row_offset = 100
alien_x_offset = 50

# alien movement tracker variable, will be used to tell when aliens switch direction of movement, initialized at 250
alien_move_tracker = 250

# global variable for the number of alien sprites (used for randomizing the sprite used)
num_alien_sprites = 3

# global variable tuples to hold the size of the sprites
alien_size = (75,75)
player_size = (50,50)
bullet_size = (10,30)
'''
Note about sprites: when a sprite is rendered onto the screen, the coordinates plugged in correspond to
                    the top left corner of the sprite. This means spawning a sprite at (0,0) will spawn the sprite
                    so that the top left corner is at (0,0) and the bottom right is at (sprite_width, sprite_height)
'''
# global variable for bullet spawn offset (to center the spawn location on the center of the player sprite)
bullet_offset = player_size[0]/2.5

# global variable for the level, starts at 0
level = 0
# global variables for level height and level message height
# top right corner
level_pos = (board_width-50, 5)
level_msg_pos = (250, 200)

# function to display level
def show_level():
    global level
    level_text = font.render("Level " + str(level), True, white)
    board.blit(level_text, level_pos)

# global varibale for score and score position
score = 0
score_pos = (5,5)

# function to display the score
def show_score():
    global score
    score_text = font.render("Score: " + str(score), True, white)
    board.blit(score_text, score_pos)

# SHIP (PLAYER) OBJECT
class ship:
    # player object will be created with these attributes
    speed = 0 #defines how the player will currently move
    speed_multiple = 3 #defines how fast the player moves
    x_pos = 575 #initial x_value, will be modified with movement keys
    y_pos = 750 #will not change; ship does not move up and down
    # NOTE: Player position should have an x-value between around 0-800 and a y-value of around 700 to stay
    #       on the board (will vary based on size of sprite)
    max_x = 1200
    min_x = 0
    image = pygame.image.load('test.png') #image for the ship, placeholder right now
    # rescale image
    image = pygame.transform.scale(image, player_size)

    # functions for the ship
    
    # function to move the ship
    def move(ship):
        # ship moves along the x-axis, so add the speed to the x-position
        ship.x_pos += ship.speed

        #if player hits end of screen, keep on screen

        #if too far left, set to min_x
        if player.x_pos <= player.min_x:
            player.x_pos = player.min_x
        
        #if too far right, set to max_x
        elif player.x_pos >= player.max_x:
            player.x_pos = player.max_x

# ALIEN OBJECT
class alien:
    global level # will be used to initialize attributes, health(?) and speed 
    global num_alien_sprites 
    # Any alien created will be initialized with these attributes
    speed = -level/2 # speed of aliens will scale on level (speed will be half of the level number) note that this starts negative
                     # as aliens will move to the left first
    y_change = 50
    health = 1 # number of shots it will take to kill (may implement health scaling later)
    # each alien will have an x and y position, will be initialized at 0 for now
    x_pos = 0
    y_pos = 0
    # sprite will be a random image generated using the randint() method from the random module
    image = pygame.image.load('alien' + str(random.randint(1, num_alien_sprites)) + '.png')
    image = pygame.transform.scale(image, alien_size)

    # function for alien movement; aliens will move like classic space invaders (sideways until hitting a wall, down a row, then other side and repeat)
    def move(aliens):
        # Note: this function moves all aliens
        # iterator variable and global move tracker
        i = 0
        global alien_move_tracker

        # every instance of movement will start with incrementing alien move tracker by the speed of the aliens (using the first alien's speed but doesn't matter since all equal)
        alien_move_tracker += aliens[i].speed
        # if hit an edge, flip the speed 
        # note: There is about 250 units to the left and 250 units to the right open when the aliens spawn. since they move left
        #       first, tracker will trigger when reaching 50 (all the way to the left) or 425 (all the way right, sum of free space), accounting for sprite size
        if alien_move_tracker <= 50 or alien_move_tracker >= 425:
            # loop to change each alien's speed to the opposite direction using global variable and increment their y-value
            while i < starting_aliens:
                # multiply speed value by -1 to flip direction
                aliens[i].speed *= -1
                # add the height of the alien to y_pos to make alien move down
                aliens[i].y_pos += alien_size[1]
                i += 1
            # reset iterator
            i = 0
            # set tracker to 50 or 425 in case it went past
            if alien_move_tracker <= 50:
                alien_move_tracker = 50
            else:
                alien_move_tracker = 425   

        # Aliens will move according to their speed
        # loop to move all aliens using global variable
        while i < starting_aliens:
            aliens[i].x_pos += aliens[i].speed
            i += 1
        

# BULLET OBJECT
class bullet:
    #NOTE: can only fire 1 bullet at a time
    speed = 12
    starting_y_pos = 700 #value to initialize y-position to when fired
    min_y = 0 #value at when the bullet reaches end of the screen
    x_pos = 2000 #this will be initialized based on the player's current position when fired, when not fired, it "hides" off screen
    y_pos = 0 #always starts at this value (hides off screen when not fired) and will be initialized when fired
    image = pygame.image.load('test.png') #image for bullet, placeholder right now
    # rescale image
    image = pygame.transform.scale(image, bullet_size)

    #function to initialize bullet
    def init(bullet, new_x_pos):
        # takes the player's current x-position and uses it as its own
        bullet.x_pos = new_x_pos + bullet_offset
        # initialize starting y-position
        bullet.y_pos = bullet.starting_y_pos
    
    #function for bullet movement (will only run if global firing = True)
    def move(bullet):
        #bullet fires down the y-axis, so movement will subtract speed value from its current y-position
        bullet.y_pos -= bullet.speed

        #if it reaches the end of the screen, set global firing variable to false and hide bullet off screen
        if bullet.y_pos <= bullet.min_y:
            global firing
            bullet.x_pos = 2000
            bullet.y_pos = 2000
            firing = False
    
# function to spawn aliens
def spawn_aliens():
    # starting_aliens will be needed to know how many new aliens to initialize
    global starting_aliens

    #these globals will be used to initialize the new positions of aliens
    global alien_x_offset
    global alien_row_offset

    # these globals will be altered
    global num_aliens
    global aliens

    # iterator variable
    i = 0
    # variable used for spawning a "5 row" (see logic below)
    five_row = 0

    # variables for first alien position and previous alien position (will be used in loop)
    first_pos = (200, 50) # leaves 200 units from the wall and sprite is 50x50, so this will spawn on the screen
    previous_pos = (0,0)

    # first if not divisible by 10, subtract 5 and store '5' in variable 'five_row' (see logic below)
    if starting_aliens % 10 != 0:
        starting_aliens -= 5
        five_row = 5

    # only do this if there are more than 5 aliens
    if starting_aliens != 0:
        # do first alien outside of the loop as it will use the variable first_pos
        # Note: aliens will render from top left across and down
        new_alien = alien()

        # assign the x and y positions of the new alien using first_pos
        new_alien.x_pos = first_pos[0]
        new_alien.y_pos = first_pos[1]

        # assign speed
        new_alien.speed = -level/2

        # append this alien to the aliens array
        aliens.append(new_alien)

        # set previous position variable to first position variable
        previous_pos = first_pos

        #increment iterator variable
        i += 1

    # loop to initialize each new alien after the first
    while i < starting_aliens:
        #create new alien
        new_alien = alien()

        # now have to determine and set its starting position:
        ''' 
        LOGIC:
                - Each row can hold 10 aliens
                - Aliens will always be in multiples of 5
                - If divisible by 10, each line will have 10 each (up to 3 rows since aliens cap at 30)
                - If not divisible by 10, there will be one row of 5 (front most row) and each otehr row will have 10
                - In the row of 5, the x offset between aliens will be multiplied by 2.43
                - Each row will leave 200 units on the left side free (distance from last alien to wall) this was done with the first alien
                - To initialize the position of each new alien, add the x offset for each new alien and add the y offset every 10
                - Every 10, will start initializing from the new row on the left
        '''

        # if the iterator variable is divisible by 10, it means new row
        if i % 10 == 0:
            # first alien of this row will have same x_pos as first_pos and a y_pos of the previous alien's plus the offset
            new_alien.x_pos = first_pos[0]
            new_alien.y_pos = previous_pos[1] + alien_row_offset
        # if not divisible by 10 set new alien position based on previous alien's position (prev x + x offset + width of alien divided by 2)
        else:
            new_alien.x_pos = previous_pos[0] + alien_x_offset + alien_size[0]/2
            new_alien.y_pos = previous_pos[1] 
        
        # generate a new sprite
        new_alien.image = pygame.image.load('alien' + str(random.randint(1, num_alien_sprites)) + '.png')
        new_alien.image = pygame.transform.scale(new_alien.image, alien_size)

        # assign speed
        new_alien.speed = -level/2

        # append new alien to the aliens array
        aliens.append(new_alien)

        # set previous position equal to the new alien jsut initialized and increment iterator variable
        previous_pos = (new_alien.x_pos, new_alien.y_pos)
        i += 1
        
    # if there was an extra 5, initialize them now
    if five_row:
        # add the 5 back to starting_aliens
        starting_aliens += five_row

        # do the first outside of the loop, same logic as above
        new_alien = alien()
        new_alien.x_pos = first_pos[0]
        new_alien.y_pos = previous_pos[1] + alien_row_offset
        new_alien.image = pygame.image.load('alien' + str(random.randint(1, num_alien_sprites)) + '.png')
        new_alien.image = pygame.transform.scale(new_alien.image, alien_size)
        new_alien.speed = -level/2
        aliens.append(new_alien)
        previous_pos = (new_alien.x_pos, new_alien.y_pos)

        # decrement five_row (will be used as iterator variable for this loop)
        five_row -= 1

        # loop to initialize, same logic as previous loop but x offset multiplied by 2.43 and + the width of an alien
        while five_row > 0:
            new_alien = alien()
            new_alien.x_pos = previous_pos[0] + alien_x_offset * 2.43 + alien_size[0]
            new_alien.y_pos = previous_pos[1]
            new_alien.image = pygame.image.load('alien' + str(random.randint(1, num_alien_sprites)) + '.png')
            new_alien.image = pygame.transform.scale(new_alien.image, alien_size)
            new_alien.speed = -level/2
            aliens.append(new_alien)
            previous_pos = (new_alien.x_pos, new_alien.y_pos)
            five_row -= 1

    # set the number of current aliens equal to the number of starting aliens
    num_aliens = starting_aliens

# function that will be called if a key is pressed. Either player movement of shooting
# parameters: keypress holds the type of key that was pressed, player is of type ship, bullet is of type bullet
def keypressed(keypress, player: ship , bullet: bullet ):
    global firing
    # if left arrow key was pressed, player moves left based on speed value
    if keypress.key == pygame.K_LEFT:
        # modify player speed value
        player.speed = -player.speed_multiple

    # if right arrow key, player moves right based on speed value
    elif keypress.key == pygame.K_RIGHT:
        # modify player speed value
        player.speed = player.speed_multiple

    # if space bar is pressed, bullet is fired if noe is not already fired
    elif keypress.key == pygame.K_SPACE:
        if firing == False:
            bullet.init(player.x_pos)
            firing = True

# function to display objects
def display(object):
    board.blit(object.image, (object.x_pos, object.y_pos))

# function to display all aliens
def display_aliens(aliens):
    # global and iterator variables needed
    global starting_aliens
    i = 0

    # loop to display all aliens
    while i < starting_aliens:
        display(aliens[i])
        i += 1

# function to proceed to next level
def level_up():
    global level
    global starting_aliens
    global level_msg_pos
    # initialize the message variable which will be usedto display a message to the player
    message = ''

    # beginning of level info messages
    if level == 1:
        # level 1 info message describes how to play
        message = "Welcome to Face Invaders! Use Left and Right Arrow Keys to Move Use Spacebar to Shoot! Destroy all the Face Invaders!"
        # increment starting aliens by 6
        starting_aliens += 5
    elif level >= 2 and level <= 6:
        # level 2-6 info message (increased aliens and speed)
        message = "Increased Number of Face Invaders and Increased Face Invader Speed"
        #increase the number of starting aliens
        starting_aliens += 5
        # change the level msg position x value
        level_msg_pos = (400, 250)
    elif level > 6:
        # level 5 and up info (maybe inmplement health scaling here)
        message = "Increased Face Invader Speed"
        # change the level msg position x value
        level_msg_pos = (512, 250)

    # display message
    level_message = font.render(message, True, white)
    board.blit(level_message, level_msg_pos)

    # update display, wait until player presses a key to continue
    wait = True
    cont_msg = font.render("Press Any Key to Continue", True, white)
    board.blit(cont_msg, (525,500))
    pygame.display.update()
    while wait == True:
        for event in pygame.event.get():
            # wait for key press and release to continue
            if event.type == pygame.KEYUP:
                wait = False

# function to see if an alien was hit
def checkHit(bullet: bullet, aliens):
    # firing, score, and num_aliens will be modified if hit is successful
    global firing
    global score
    global num_aliens
    '''
    Recalling that an object's position is in the top left corner of its sprite, a range of values needs to be chacked for a hit.
    For this game, if any part of the projectile touches the alien, it will be considered a hit. What this means is that the x-values
    to be checked for a hit are:
        - from the x-position of the alien to the x-position of the alien plus alien width (this covers the width of the alien)
        - from the x-position of the alien to the x-position of the alien minus the width of projectile (covers if the projectile
          makes partial contact with the alien on the left side)
    Also for the purposes of this game, only the bottom half of the alien will be considered hittable. This means if the top half
    of the alien runs into the projectile, it will not count as a hit (this avoids hits that don't seem like they should have counted)
        - since object position is at top left, bottom height can be found by subtracting alien height from y-position
        - half height can be found by subtracting half the height
    '''
    # iterator variable
    i = 0
    # loop to check each alien using global variable
    while i < starting_aliens:
        # see if x position lines up
        if aliens[i].x_pos - bullet_size[0] < bullet.x_pos and aliens[i].x_pos + alien_size[0] > bullet.x_pos:
            # see if y position lines up
            if aliens[i].y_pos - alien_size[1] <= bullet.y_pos and aliens[i].y_pos - alien_size[1]/2 >= bullet.y_pos:
                # this is a successful hit. increment the score by 1 times the level (just add level) and decrement num aliens
                score += level
                num_aliens -= 1
                # set firing to false
                firing = False

                # bullet and alien hit need to disappear. Hide them at (2000, 0)
                bullet.x_pos = 2000
                bullet.y_pos = 0
                aliens[i].x_pos = 2000
                aliens[i].y_pos = 0

        # exit loop  
        if firing == False:
            break
        i += 1
            
# function to determine if player loses
def game_over(aliens):
    # if player loses and choses t oquit, running will be modified
    global running

    # if player choses to play again, the following will be modified
    global level
    global starting_aliens
    global num_aliens
    global score

    # variable will be used to break loop
    lost = False 

    # if an alien passes the y value of the player, player loses
    # iterator variable
    i = 0
    while i < starting_aliens:
        if aliens[i].y_pos > ship.y_pos:
            # if player lost, display a game over message along with score
            fail_text = fail_font.render("GAME OVER", True, red)
            board.blit(fail_text, (500, 200))
            final_score = font.render("Score: " + str(score), True, white)
            board.blit(final_score, (600, 500))

            # variable will be used to break loop
            lost = True

            # display play again or quit
            play_again = font.render("Press Q to quit or any other key to play again", True, white)
            board.blit(play_again, (400, 600))

            # wait for response
            wait = True
            # refresh the display
            pygame.display.update()
            # wait 1.5 seconds before taking any inputs (due to accidental keypress when losing (i.e. frantic spacebar spamming))
            pygame.time.wait(1500)
            while wait == True:
                for event in pygame.event.get():
                # wait for key press and release to continue
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_q:
                            # if they chose to quit, end game loop
                            running = False
                        else:
                            # if play again, reset game
                            level = 0
                            score = 0
                            num_aliens = 0
                            starting_aliens = 0
                        wait = False
        
        if lost:
            break
        i += 1



# Variable which will hold whether game is running or not (keeps game loop on or turns it off when game is closed)
running = True

# create objects
player = ship()
projectile = bullet()
# array of aliens
aliens = []
# img_test = pygame.image.load('test.png')
# img_pos = (780,700)
# board.blit(img_test,img_pos)
# pygame.display.update()

# create a loop for the game
while running:

    # start each loop by creating "blank slate", this essentially removes all images from previous loop so new ones can
    # be added over top, creating movement
    board.fill(black)
    # detect an event
    for event in pygame.event.get():

        # if event was quitting, end loop, close game
        if event.type == pygame.QUIT:
            running = False

        # event was a keypress, call keypressed function to determine action
        if event.type == pygame.KEYDOWN:
            keypressed(event, player, projectile)
        
        #if key is released, check to see if it was a movement key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # if movement key released, set speed to 0
                player.speed = 0

    #if a bullet is being fired, move the bullet
    if firing == True:
        projectile.move()
    
    #check if projectile hit
    checkHit(projectile, aliens)

    #move player
    player.move()

    display(player)
    display(projectile)
    show_score()

    # check for a game over
    game_over(aliens)

    # if the current number of aliens is 0, level is passed, start the level up sequence
    if num_aliens == 0:
        # increment level
        level += 1
        # show the level and update display to reflect the change
        show_level()
        pygame.display.update()
        # call the level_up function
        level_up()
        # spawn aliens for next level
        # delete and re initialize aliens array
        del aliens
        aliens = []
        spawn_aliens()
    
    show_level()
    #move aliens
    alien.move(aliens)
    display_aliens(aliens)
    pygame.display.update()