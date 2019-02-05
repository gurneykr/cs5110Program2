import random, pygame, sys
from pygame.locals import *

FPS = 7
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BROWN     = (128,  0,    0)
BLUE     =  (  0, 255, 255)
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
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    roombaCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the dirt in a random place.
    dirt = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                pass
                # if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                #     direction = LEFT
                # elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                #     direction = RIGHT
                # elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                #     direction = UP
                # elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                #     direction = DOWN
                # elif event.key == K_ESCAPE:
                #     terminate()

        # newHead = {'x': roombaCoords[HEAD]['x'], 'y': roombaCoords[HEAD]['y']}

        # check if the worm has hit itself or the edge
        if roombaCoords[HEAD]['x'] == -1 or roombaCoords[HEAD]['x'] == CELLWIDTH or roombaCoords[HEAD]['y'] == -1 or roombaCoords[HEAD]['y'] == CELLHEIGHT:
            newHead = rotateRoomba(direction, roombaCoords)
        else:
            if direction == UP:
                newHead = {'x': roombaCoords[HEAD]['x'], 'y': roombaCoords[HEAD]['y'] - 1}
            elif direction == DOWN:
                newHead = {'x': roombaCoords[HEAD]['x'], 'y': roombaCoords[HEAD]['y'] + 1}
            elif direction == LEFT:
                newHead = {'x': roombaCoords[HEAD]['x'] - 1, 'y': roombaCoords[HEAD]['y']}
            elif direction == RIGHT:
                newHead = {'x': roombaCoords[HEAD]['x'] + 1, 'y': roombaCoords[HEAD]['y']}

        # check if worm has eaten an apply
        if roombaCoords[HEAD]['x'] == dirt['x'] and roombaCoords[HEAD]['y'] == dirt['y']:
            # don't remove worm's tail segment
            dirt = getRandomLocation() # set a new dirt somewhere
        else:
            del roombaCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        # if direction == UP:
        #     newHead = {'x': roombaCoords[HEAD]['x'], 'y': roombaCoords[HEAD]['y'] - 1}
        # elif direction == DOWN:
        #     newHead = {'x': roombaCoords[HEAD]['x'], 'y': roombaCoords[HEAD]['y'] + 1}
        # elif direction == LEFT:
        #     newHead = {'x': roombaCoords[HEAD]['x'] - 1, 'y': roombaCoords[HEAD]['y']}
        # elif direction == RIGHT:
        #     newHead = {'x': roombaCoords[HEAD]['x'] + 1, 'y': roombaCoords[HEAD]['y']}

        roombaCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(roombaCoords)
        drawDirt(dirt)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def rotateRoomba(direction, roombaCoords):
    if direction == RIGHT: #turn down
        newHead = {'x': roombaCoords[HEAD]['x'], 'y': roombaCoords[HEAD]['y'] + 1}
    elif direction == DOWN: #turn left
        newHead = {'x': roombaCoords[HEAD]['x'] - 1, 'y': roombaCoords[HEAD]['y']}
    elif direction == LEFT:#turn up
        newHead = {'x': roombaCoords[HEAD]['x'], 'y': roombaCoords[HEAD]['y'] - 1}
    elif direction == UP:#turn right
        newHead = {'x': roombaCoords[HEAD]['x'] + 1, 'y': roombaCoords[HEAD]['y']}
    return newHead

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
        FPSCLOCK.tick(FPS)
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


def drawWorm(roombaCoords):
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


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()