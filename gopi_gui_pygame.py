import random, pygame, sys
from pygame.locals import *
from math import *

from sms.sms_hub_lib4 import SmsTcpClient
from sms.sms_pi import Disp_sm_pi
import time 

import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
 



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
serv_temp2 = 1
gopi_volt = ''
gopi_fwd = None


def Disp_sm_gui(fra, til, data, con):
    global serv_temp, serv_temp2, gopi_volt
    
    rdata = None
    #print fra, til, data
    if til[0] == 'STemp':
        serv_temp = data
    elif til[0] == 'STemp2':
        serv_temp2 = data
    elif til[0] == 'GVolt':
        gopi_volt = data
    elif til[0] == 'ping':
        #conDict[data] = sms_client(data, '', con)
        rdata = 'ACK'
        print conDict
    else:
        #print 'DISP_SM'
        rdata = Disp_sm_pi(fra, til, data, con)
            
    return rdata
    
    
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, cli, rpc

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('GoPiGo - Gui')
    
    cli = SmsTcpClient( "gui", '192.168.1.166', 9999)
    rpc = SmsTcpClient( "gui-rpc", '192.168.1.166', 9999)

    #showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def senterPos(m_pos):            
    mx = (m_pos[0] - WINDOWWIDTH/2)
    my = (m_pos[1] - WINDOWHEIGHT/2)
    return mx, my


def compSpd(m_pos):
    aspd =   -(m_pos[1] - WINDOWHEIGHT/2)/2 + (m_pos[0] - WINDOWWIDTH/2)/4
    dspd =   -(m_pos[1] - WINDOWHEIGHT/2)/2 - (m_pos[0] - WINDOWWIDTH/2)/4
        
    if not gopi_fwd:
        aspd = -aspd
        dspd = -dspd
        
    if aspd < 0:
        dspd -= aspd
        aspd = 0
    if dspd < 0:
        aspd -= dspd
        dspd = 0
            
    return aspd, dspd
  
  
class ShowList(object):
    
    def __init__(self, x, y, ant):
        self.data = []
        self.x = x
        self.y = y
        
    def clr(self):
        data = []
          
    def drawLine(self, i, line):
        scoreSurf = BASICFONT.render('%d: %s' % (i, line), True, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 220, 10 + i*20)
        DISPLAYSURF.blit(scoreSurf, scoreRect)    
    
    
class PingGrf(object):

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.data1 = []
        self.data2 = []
        self.surf = None
        
        for i in xrange(0, size):
            self.data1.append( sin(i*90) )
            self.data2.append( sin(i*90) )
            
        self.fig = pylab.figure(figsize=[3, 1.5], # Inches
                   dpi=100,   )
        self.ax = self.fig.gca()

    def draw(self):
        DISPLAYSURF.blit(self.surf, (0,0))

        
    def make(self):

        self.ax.clear()
        self.ax.plot(self.data1)
        self.ax.plot(self.data2)
         
        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb() 
        size = canvas.get_width_height()
        self.surf = pygame.image.fromstring(raw_data, size, "RGB")
        #ax.close()
        
        
    def addData1(self, val):
        
        print int(val)
        self.data1 = self.data1[1:] + [int(val)]
        #self.make()

    def addData2(self, val):
        
        print int(val)
        self.data2 = self.data2[1:] + [int(val)]
        #self.make()


            
def runGame():
    global serv_temp, serv_temp2, gopi_volt, gopi_fwd
    
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
    m_pos = (-1,-1)
    m_pos_last = (-1,-1)
    m_down = None
    pingGrf = PingGrf('Ping', 100)
    pingGrf.make()
    
    img=pygame.image.load('test.jpg')
    
    FPS = 5

    while True: # main game loop
        loopCnt += 1
        
        while cli.disp_sms(Disp_sm_gui) == True:
            pass
        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a):
                    cli.sendSM('GVolt', 'GoPiGo.cmd.a', '.')
                elif (event.key == K_RIGHT or event.key == K_d):
                    cli.sendSM('GVolt', 'GoPiGo.cmd.d', '.')
                elif (event.key == K_UP or event.key == K_w):
                    cli.sendSM('GVolt', 'GoPiGo.cmd.w', '.')
                elif (event.key == K_DOWN or event.key == K_s):
                    cli.sendSM('GVolt', 'GoPiGo.cmd.s', '.')
                elif (event.key == K_t):
                    cli.sendSM('GVolt', 'GoPiGo.cmd.t', '.')
                    
                elif (event.key == K_p):
                    #cli.sendSM('GVolt', 'GoPiGo.ping', '.')
                    t0 = time.time()
                    cli.sm_func(cli.name, 'GoPiGo.ping', '.')
                    time.sleep(0.1)
                    print 'ping: ', (time.time() - t0)*100, 'ms' 
                elif (event.key == K_o):
                    #cli.sendSM('GVolt', 'GoPiGo.ping', '.')
                    t0 = time.time()
                    cli.sm_func(cli.name, 'Serv.ping', '.')
                    pingGrf.addData((time.time() - t0)*100)
                    #time.sleep(0.1)
                    print 'ping: ', (time.time() - t0)*100, 'ms' 

                elif (event.key == K_g):
                    cli.sendSM('GVolt', 'GoPiGo.cmd.g', '.')
                elif (event.key == K_e):
                    cli.sendSM('GVolt', 'GoPiGo.cmd.b', '.')
                    serv_temp = ''                    
                    serv_temp2 = ''
                    gopi_volt = ''
                elif (event.key == K_r):
                    cli.sendSM('STemp', 'Serv.CpuTemp', '.')
                    cli.sendSM('STemp2', 'GoPiGo.CpuTemp', '.')
                elif (event.key == K_v):
                    cli.sendSM('GVolt', 'GoPiGo.cmd.v', '.')
                    cli.sendSM('STemp2', 'GoPiGo.CpuTemp', '.')
                elif event.key == K_ESCAPE or event.key == K_q:
                    terminate()
            elif event.type == KEYUP:
                cli.sendSM('GVolt', 'GoPiGo.cmd.x', '.')
                
            elif event.type == MOUSEMOTION:
                #print 'Mp: ', loopCnt, event.pos
                m_pos = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                #print 'Mp: ', loopCnt, event.pos
                #cli.sendSM('GVolt', 'GoPiGo.cmd.w', '.')
                m_down = True
                m_pos = event.pos    
                m_pos_last = (-1,-1)
                
                mx, my = senterPos(m_pos)
                
                if gopi_fwd and my > 0:
                    gopi_fwd = False
             #       cli.sendSM('GVolt', 'GoPiGo.cmd.s', '.') # bwd
                elif not gopi_fwd and my < 0:
                    gopi_fwd = True
             #       cli.sendSM('GVolt', 'GoPiGo.cmd.w', '.') # fwd
                    
            elif event.type == MOUSEBUTTONUP:
                #print 'Mp: ', loopCnt, event.pos
                
                cli.sendSM('GVolt', 'GoPiGo.cmd.x', '.')
                cli.sendSM('GVolt', 'GoPiGo.cmd.as', str(0))
                cli.sendSM('GVolt', 'GoPiGo.cmd.ds', str(0))
                m_down = False         
                
            else:
                print loopCnt, event 


        if m_pos <> m_pos_last:
            
            mx, my = senterPos(m_pos)
                    
            aspd, dspd = compSpd(m_pos)
            
            if m_down:        
                cli.sendSM('GVolt', 'GoPiGo.cmd.as', str(aspd))
                cli.sendSM('GVolt', 'GoPiGo.cmd.ds', str(dspd))
                
                if my >= 0:
                    gopi_fwd = False
                    cli.sendSM('GVolt', 'GoPiGo.cmd.s', '.') # bwd
                elif my < 0:
                    gopi_fwd = True
                    cli.sendSM('GVolt', 'GoPiGo.cmd.w', '.') # fwd
                     
            m_pos_last = m_pos
            print 'Mp: ', loopCnt, m_pos
            print 'go: ', loopCnt, aspd, dspd
    
    
    
    
        if loopCnt % (FPS*1) == 0: 
            
            t0 = pygame.time.get_ticks() #time.time()                
            rpc.sm_rpc('GoPiGo.ping', '.')
            td = (pygame.time.get_ticks() - t0)
            pingGrf.addData1(td)
            #time.sleep(0.1)
            print 'ping: ', td, 'ms'
            
            t0 = pygame.time.get_ticks() #time.time()                
            rpc.sm_rpc('Serv.ping', '.')
            td = (pygame.time.get_ticks() - t0)
            pingGrf.addData2(td)
            #time.sleep(0.1)
            print 'ping: ', td, 'ms'
            
            pingGrf.make()
        
        #DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(img,(0,0))
        drawGrid()
        #drawWorm(wormCoords)
        drawApple(apple)
        #drawScore(serv_temp)
        
        drawTemp(1, "SMS hub", serv_temp)
        drawTemp(2, "GoPi Temp", serv_temp2)
        drawTemp(3, "GoPi Volt", gopi_volt)
        
        pingGrf.draw()
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
    rpc = SmsTcpClient( "gui-rpc", '192.168.1.166', 9999)

    #print "## RegName: " + cli.sm_func(cli.name, 'Serv.RegName', cli.name)
    #print "## CpuTemp: " + cli.sm_func(cli.name, 'Serv.CpuTemp', '.')
    
    t0 = time.time()
    while time.time() - t0 < 0.1:
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
    global cli, rpc
    
    cli.close()
    rpc.close()
    
    #cli.sm_func(cli.name, 'Serv.UnRegName', cli.name)
    
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    #{'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


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
    x = WINDOWWIDTH / 2 #coord['x'] * CELLSIZE
    y = WINDOWHEIGHT / 2 #coord['y'] * CELLSIZE
    #appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    #pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    #pygame.draw.circle(DISPLAYSURF, RED, (x + CELLSIZE/2, y + CELLSIZE/2), CELLSIZE/2)
    pygame.draw.circle(DISPLAYSURF, RED, (x , y), CELLSIZE/2)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE*4): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x-40, 0), (x+40, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE*4): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
