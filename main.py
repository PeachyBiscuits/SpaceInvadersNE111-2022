import pygame
import math

# initialize pygame
pygame.init()

#create the "game board"
board_width = 1000
board_height = 1000


board = pygame.display.set_mode((board_width, board_height))
pygame.display.set_caption("Face Invaders - NE111")

# classes for objects that will be used in the game: Ship (player), alien, bullet

# global variable to stroe if a bullet is currently fired 
firing = False

class ship:
    speed = 0 #defines how the player will currently move
    speed_multiple = 3 #defines how fast the player moves
    x_pos = 400 #initial x_value, will be modified with movement keys
    y_pos = 700 #will not change; ship does not move up and down
    # NOTE: Player position should have an x-value between around 0-800 and a y-value of around 700 to stay
    #       on the board (will vary based on size of sprite)
    max_x = 800
    min_x = 0
    image = pygame.image.load('test.png') #image for the ship, placeholder right now

    # functions for the ship
    
    # function to move the ship
    def move(ship):
        # shup moves along the x-axis, so add the speed to the x-position
        ship.x_pos += ship.speed

        #if player hits end of screen, keep on screen

        #if too far left, set to min_x
        if player.x_pos <= player.min_x:
            player.x_pos = player.min_x
        
        #if too far right, set to max_x
        elif player.x_pos >= player.max_x:
            player.x_pos >= player.max_x
            player.x_pos = player.max_x




    #add image thingy 
class alien:
    health = 1 
    speed = 5 #this is arbitrary idk what to put 

    #add image thingy

class bullet:
    #NOTE: can only fire 1 bullet at a time
    speed = 5
    starting_y_pos = 700 #value to initialize y-position to when fired
    min_y = 0 #value at when the bullet reaches end of the screen
    x_pos = 2000 #this will be initialized based on the player's current position when fired, when not fired, it "hides" off screen
    y_pos = 2000 #always starts at this value (hides off screen when not fired) and will be initialized when fired
    image = pygame.image.load('test.png') #image for bullet, placeholder right now

    #function to initialize bullet
    def init(bullet, new_x_pos):
        # takes the player's current x-position and uses it as its own
        bullet.x_pos = new_x_pos
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

# funtion to display objects
def display(object):
    board.blit(object.image, (object.x_pos, object.y_pos))

#keep game running (debug)
running = True

# create objects
player = ship()
projectile = bullet()

# img_test = pygame.image.load('test.png')
# img_pos = (780,700)
# board.blit(img_test,img_pos)
# pygame.display.update()

# create a loop for the game
while running:
    # start each loop by creating "blank slate", this essentially removes all images from previous loop so new ones can
    # be added over top, creating movement
    board.fill((255,0,0))
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
    
    #move player
    player.move()
    display(player)
    display(projectile)
    
    pygame.display.update()