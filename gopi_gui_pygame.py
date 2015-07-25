import random, pygame, sys
from pygame.locals import *

from sms.sms_hub_lib4 import SmsTcpClient
from sms.sms_pi import Disp_sm_pi

FPS = 30

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
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head
cli = None

serv_temp = 0
serv_temp2= 1


def Disp_sm_gui(fra, til, data, con):
    global serv_temp, serv_temp2
    
    #print fra, til, data
    if til[0] == 'STemp':
        serv_temp = data
        data = None
    elif til[0] == 'STemp2':
        serv_temp2 = data
        data = None
    elif til[0] == 'ping':
        #conDict[data] = sms_client(data, '', con)
        data = 'ACK'
        print conDict
    else:
        #print 'DISP_SM'
        data = Disp_sm_pi(fra, til, data, con)
            
    return data
    
    
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('GoPiGo - Gui')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    global serv_temp, serv_temp2
    
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    loopCnt = 0
    m_pos = None
    m_pos_last = None
    FPS = 3

    while True: # main game loop
        loopCnt += 1
        
        while cli.disp_sms(Disp_sm_gui) == True:
            pass
        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif (event.key == K_t):
                    serv_temp = cli.sm_func(cli.name, 'Serv.CpuTemp', '.')
                    serv_temp2 = cli.sm_func(cli.name, 'GoPiGo.CpuTemp', '.')
                elif (event.key == K_e):
                    serv_temp = ''                    
                    serv_temp2 = ''
                elif (event.key == K_r):
                    cli.sendSM('STemp', 'Serv.CpuTemp', '.')
                    cli.sendSM('STemp2', 'GoPiGo.CpuTemp', '.')
                elif event.key == K_ESCAPE or event.key == K_q:
                    terminate()

            elif event.type == MOUSEMOTION:
                #print 'Mp: ', loopCnt, event.pos
                m_pos = event.pos
                
            else:
                print loopCnt, event 


        if m_pos <> m_pos_last:
            m_pos_last = m_pos
            print 'Mp: ', loopCnt, m_pos
        
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        #drawScore(serv_temp)
        
        drawTemp(1, "SMS hub", serv_temp)
        drawTemp(2, "GoPiGo", serv_temp2)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)



# KRT 14/06/2012 rewrite event detection to deal with mouse use
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:      #event is quit 
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   #event is escape key
                terminate()
            else:
                return event.key   #key found return with it
    # no quit or key events in queue so return None    
    return None

    
def showStartScreen():
    global cli
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('GoPiGo!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('GoPiGo!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    
#KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue
    FPS = 10

    # Conect to server
    #cli = SmsTcpClient( "cli", '127.0.0.1', 9999)
    cli = SmsTcpClient( "gui", '192.168.1.166', 9999)
    print "## RegName: " + cli.sm_func(cli.name, 'Serv.RegName', cli.name)
    print "## CpuTemp: " + cli.sm_func(cli.name, 'Serv.CpuTemp', '.')
    

    


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
#KRT 14/06/2012 rewrite event detection to deal with mouse use
        if checkForKeyPress():
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    global cli
    cli.sm_func(cli.name, 'Serv.UnRegName', cli.name)
    
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
#KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue 
    while True:
        if checkForKeyPress():
            return
#KRT 12/06/2012 reduce processor loading in gameover screen.
        pygame.time.wait(100)

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawTemp(i, servName, temp):
    scoreSurf = BASICFONT.render('%s: %s' % (servName, temp), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 220, 10 + i*20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    #appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    #pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    pygame.draw.circle(DISPLAYSURF, RED, (x + CELLSIZE/2, y + CELLSIZE/2), CELLSIZE/2)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
