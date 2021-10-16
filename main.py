import random    # for generating random numbers
import sys    # to use sys.exit() to exit the program()
import pygame
from pygame.locals import *    # basic pygame imports


# Global Variables for the game
FPS = 32    # 32 images per second
SCREENWIDTH = 289    # width of the screen
SCREENHEIGHT = 511    # height of the screen
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8    # y coordinate of the ground will be 80 % of screenheight
GAME_SPRITES = {}    # list containing all the sprites for the game
GAME_SOUNDS = {}    # list containing all the sounds for the game
PLAYER = 'gallery/sprites/bird.png'    # full path of the image of the player
BACKGROUND = 'gallery/sprites/background.png'    # full path of the background image
PIPE = 'gallery/sprites/pipe.png'    # full path of the image of the pillars


def text_screen(name, text, color, x, y, size, b=False, i=False):
        font = pygame.font.SysFont(name, size, b, italic=i)
        Screen_text = font.render(text, True, color)
        SCREEN.blit(Screen_text, (x, y))
    # name = Segoe Script


def welcomeScreen():
    """
    Shows welcome image on the screen
    """
    # playerx = int((SCREENWIDTH - GAME_SPRITES['player'].get_width())/2)    # original value would have been float, which we don't want
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)    # to get the center
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)    # to get the center
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button or presses the escape key, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()    # quit the game
                sys.exit()    # close the program
            # if user presses space or up arrow key, start the game
            elif (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or event.type == MOUSEBUTTONDOWN:
                return    # moves the control to line next to the function call
            # if the user presses nothing, keep showing the welcome screen
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    # SCREEN.blit(path_of_image, coordinate)
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    # y will be same as that of the ground
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['r'], (messagex, messagey + 100))
                text_screen("Segoe UI", "by", (0, 0, 0), messagex - 2, (50 + messagey + 10), 19, b=True, i=True)
                text_screen("Segoe UI", "Priyangshu", (25, 125, 25), messagex + 32, (50 + messagey), 30, b=True)
                SCREEN.blit(GAME_SPRITES['tap'], ((SCREENWIDTH - GAME_SPRITES['tap'].get_width())/2, playery + 45))
                pygame.display.update()    # if the display is not updated, no blit will occur
                FPSCLOCK.tick(FPS)    # set the no. of blits per second


def mainGame():
    score = 0    # initialize the score
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)    # to get the center coordinate
    basex = 0

    # create two pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of lower pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    # list of upper pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4    # number of pixels the pipes will move per second

    playerVelY = -9    # velocity of the bird
    playerMaxVelY = 10    # maximum velocity the bird can acquire; if not limited, the bird will enter space!
    playerMinVelY = -8    # minimum velocity of the bird
    playerAccY = 1    # accelaration of the bird

    playerFlapAccv = -8    # velocity while flapping
    playerFlapped = False    # it will be true only when the bird will be flapping


    while True:    # Game loop
        for event in pygame.event.get():
            # if user clicks on cross button or presses the escape key, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or event.type == MOUSEBUTTONDOWN:
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:    # if collision occurs, shift the control to the line next to the function call
            return

        # check for score
        playerMidPosition = playerx + GAME_SPRITES['player'].get_width()/2    # width-wise center of the bird
        for pipe in upperPipes:
            pipeMidPosition = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2    # width-wise center any pipe
            if pipeMidPosition <= playerMidPosition < pipeMidPosition + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        # if velocity of player is lesser than the maximum velocity, and player is not flapping,
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY    # accelerate its fall

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # add a pair of pipes to the right if the pipes to left are about to get out of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit our sprites now!
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        # Blitting the score
        MyDigit = []
        for digit in list(str(score)):    # convert the score to str(iterable) and then str to list. 12 -> ("1", "2")
            MyDigit.append(int(digit))    # append the integer form of the elements of the list. ("1", "2") -> (1, 2)

        # Logic for taking x coordinate such that the score is in center
        width = 0    # initialize variable holding width of the images of the digit of the number
        for d in MyDigit:
            width += GAME_SPRITES['numbers'][d].get_width()    # 2.png for 2, as 'numbers'[2] = 2.png

        scoreX = (SCREENWIDTH - width)/2    # x coordinate of the score will be central!

        # finally, score(the digits) will be blitted:
        for digit in MyDigit:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (scoreX, SCREENHEIGHT*0.12))    # y coordinate can be anything!
            scoreX += GAME_SPRITES['numbers'][digit].get_width()    # increase x for the next digit by this one's width

        pygame.display.update()    # don't forget to update!
        FPSCLOCK.tick(FPS)    # to control the speed of iteration of the while loop


def isCollide(playerx, playery, upperPipes, lowerPipes):
    # if bird touches the ground or the roof, return True, i.e., collision occurred
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery <= pipeHeight + pipe['y']) and (abs(playerx - pipe['x']) <= GAME_SPRITES['player'].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() >= pipe['y']) and (abs(playerx - pipe['x']) <= GAME_SPRITES['player'].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    """
    :return: a list containing two dictionaries; a dictionary contains x and y coordinate for the upper pillar,
             and the other dictionary contains x and y coordinates for the lower pillar; all the coordinates
             are random, though sensible.
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipex = SCREENWIDTH + 10
    y1 = offset + pipeHeight - y2
    pipe = [
        {'x': pipex, 'y': -y1},    # upper pipe, hence negative value for y
        {'x': pipex, 'y': y2}    # lower pipe
    ]
    return pipe


if __name__ == "__main__":
    # this will be the main function from where the game will start
    pygame.init()    # initialize all modules of pygame
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (    # there will be 2 pipes, one attached to the top, one to the bottom
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),    # rotate 180 degrees
        pygame.image.load(PIPE).convert_alpha()
        )
    GAME_SPRITES['tap'] = pygame.image.load('gallery/sprites/t.png').convert_alpha()
    GAME_SPRITES['r'] = pygame.image.load('gallery/sprites/r.png').convert_alpha()

    # Game Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()    # shows welcome screen until a button is pressed
        mainGame()    # this is the main game function
