import random, pygame, sys
from pygame.locals import *

#FPS = 14
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)#24
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)#32

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BROWN     = (128,  0,    0)
BLUE     =  (  0, 255, 255)
DARKBLUE =  (0,   0,   225)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Roomba')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.

    roombaCoords = [{'x': 0, 'y': 0}]
    direction = RIGHT

    barrier_list = []

    for i in range(random.randint(3, 7)):
        barrier_list.append(getRandomLocation())

    # Start the dirt in a random place.
    dirt_list = []
    for i in range(random.randint(1, 10)):
        dirt_list.append(getRandomLocation())

    count = 0

    go_left_flag = False
    go_right_flag = False
    go_down_flag = False
    go_up_flag = False

    while True: # main game loop

        for event in pygame.event.get(): # event handling loop

            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                pass

        # if (count % 35) == 0:
        #    direction = randomDirection()
        # # check if the worm has hit itself or the edge

        x = roombaCoords[HEAD]['x']
        y = roombaCoords[HEAD]['y']

        if go_left_flag == True:
            direction = LEFT
            go_left_flag = False
        if go_right_flag == True:
            direction = RIGHT
            go_right_flag = False
        if go_down_flag == True:
            direction = DOWN
            go_down_flag = False
        if go_up_flag == True:
            direction = UP
            go_up_flag = False
        else:
            if roombaCoords[HEAD]['x'] <= -1:#hit the left wall
                x = 0
                direction = DOWN
                go_right_flag = True
            if roombaCoords[HEAD]['x'] >= CELLWIDTH:#hit the right wall
                x = CELLWIDTH - 1
                direction = DOWN
                go_left_flag = True
            if roombaCoords[HEAD]['y'] <= -1:#hit the top wall
                y = 0
                direction = RIGHT
                go_down_flag = True
            if roombaCoords[HEAD]['y'] >= CELLHEIGHT:#hit the bottom wall
                y = CELLHEIGHT - 1
                direction = RIGHT
                go_up_flag = True

        for barrier in barrier_list:
            if roombaCoords[HEAD]['x'] == barrier['x'] and roombaCoords[HEAD]['y'] == barrier['y']:
                if direction == LEFT:  # if it hit on the right side go down then left
                    direction = DOWN
                    go_left_flag = True
                elif direction == RIGHT:  # if hit on the left side go down then right
                    direction = DOWN
                    go_right_flag = True
                elif direction == DOWN: #if hit on the top side go right then down
                    direction = RIGHT
                    go_down_flag = True
                elif direction == UP: #if hit on the bottom side go left then up
                    direction = LEFT
                    go_up_flag = True

        if direction == UP:
            newHead = {'x': x, 'y': y - 1}
        elif direction == DOWN:
            newHead = {'x': x, 'y': y + 1}
        elif direction == LEFT:
            newHead = {'x': x - 1, 'y': y}
        elif direction == RIGHT:
            newHead = {'x': x + 1, 'y': y}

        FPS = 14
        # check if worm has eaten an apply
        for dirt in dirt_list:
            if roombaCoords[HEAD]['x'] == dirt['x'] and roombaCoords[HEAD]['y'] == dirt['y']:
                dirt_list.remove(dirt)
                FPS = 1
                # del roombaCoords[-1]  # remove worm's tail segment
        del roombaCoords[-1] # remove worm's tail segment

        if len(dirt_list) == 0:
            print("all done")
            newHead = {'x': 0, 'y': 0}
            # return

        roombaCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawBattery({'x': 0, 'y': 0})
        drawBattery({'x': 1, 'y': 0})
        drawBattery({'x': 0, 'y': 1})
        drawBattery({'x': 1, 'y': 1})

        for dirt in dirt_list:
            drawDirt(dirt)

        drawRoomba(roombaCoords)
        for barrier in barrier_list:
            drawBarrier(barrier)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # count += 1
        # print("count: ", count)

def randomDirection():
    direction = random.randint(1, 4)
    if direction ==1:
        newDirection = UP
    elif direction == 2:
        newDirection = RIGHT
    elif direction == 3:
        newDirection = DOWN
    elif direction == 4:
        newDirection = LEFT
    return newDirection


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Roomba!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Roomba!', True, BLUE)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(14)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

# def drawScore(score):
#     scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
#     scoreRect = scoreSurf.get_rect()
#     scoreRect.topleft = (WINDOWWIDTH - 120, 10)
#     DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawBattery(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    dirtRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, DARKBLUE, dirtRect)

def drawRoomba(roombaCoords):
    for coord in roombaCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawDirt(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    dirtRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, BROWN, dirtRect)

def drawBarrier(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    dirtRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, BLUE, dirtRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()