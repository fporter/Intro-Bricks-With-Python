from livewires import games, colour
import random

#                           --Bricks--
#       Move slider bar across the screen and hit bricks to
#       break them. Has breakable bricks of n levels, bricks
#       that drop items
#                           --Board--
#       number = number of hits it takes to break a brick, 1-9
#       *number = brick with an item and takes that many hits, 1-9
#
#                           --Items-- has the ability to add these as-is
#       Multiballs: adds two other balls to the game
#       Save:       Bounces back from the dead
#       Extra life: adds a ball
#
#       Also has the ability to load from a file
#

# brick class
class brick(games.Sprite):

    # get item number and number of licks it takes
    def __init__(self, screen, x, y,image, numOfHits = 1, hasItem = False):
        self.isDrop = hasItem
        self.licksToTheCenter = numOfHits
        self.init_sprite(screen=screen,x=x,y=y,image=image)
        global brickCount
        try:
            if brickCount is None:
                brickCount = 0
        except(NameError):
            brickCount = 0
        brickCount = brickCount + 1
        
    # Is it breakable
    def isBreakable(self):
        if self.licksToTheCenter is not 0:
            return True
        else:
            return False

    # Does it drop an item, if so returns random item number
    def item(self):
        if self.__isDrop and self.isBreakable():
            return random.randrange(3)+1
        else:
            return False
    def hit(self):
        if self.licksToTheCenter is 1:
            global brickCount
            brickCount = brickCount - 1
            if brickCount is 0:
                games.Message(self.screen,725/2,725/2,"You Win at Life",70,colour.white,25000,self.screen.quit())
            self.destroy()
        else:
            self.licksToTheCenter = self.licksToTheCenter - 1
            self.replace_image(brickImgs[self.licksToTheCenter])
            
        return

    # How many licks to get to the center ? 1.. 2.. 3...
    def howManyHits(self):
        return self.licksToTheCenter

    def __str__(self):
        return "(" + str(self.licksToTheCenter) + ", " + str(self.__isDrop) + ")"

    def __repr__(self):
        return "(" + str(self.licksToTheCenter) + ", " + str(self.__isDrop) + ")"
    
# base class for item
class item:
    def isAItem(self):
        return False

# ball
class ball(item, games.Sprite, games.Mover):

    # shouldn't need to take anything, just makes varibles
    def __init__(self,screen):
        self.init_sprite(screen=screen,x=350,y=725-44,image=games.load_image('ball.bmp'))
        self.dx = 0
        self.dy = -2
        self.init_mover(dx=self.dx,dy=self.dy)
        self.spd = 1
        self.addDir = 0
        self.screen = screen
        global ballCount
        try:
            if ballCount is None:
                ballCount = 0
        except(NameError):
            ballCount = 0
        ballCount = ballCount + 1
    def hitPaddle(self,(x,y)):
        x2,y2 = self.pos()
        self.move_to(x2,y-17)
        self.addDir = self.addDir + int((x - x2)/6)*(-1)
        if self.addDir > 9:
            self.addDir = 9
        if self.addDir < -9:
            self.addDir = -9
        self.dy=self.dy*(-1)
        self.init_mover(dx=self.dx*self.spd+self.addDir, dy=self.dy*self.spd)
        
    def hitBrick(self,brick):
        x,y = brick.pos()

        self.dx=self.dx*(-1)
        self.dy=self.dy*(-1)
        
        x2,y2 = self.pos()
        
        while((x-50 < x2+10*self.dy*(-1) and x2+10*self.dy*(-1) > 50+x)and(y-15 < y2-10*self.dx*(-1) and y2-10*self.dx*(-1) > 15+y )):
            self.init_mover(dx=self.dx*self.spd+self.addDir*(-1), dy =self.dy*self.spd)
        self.init_mover(dx=0, dy =0)

        x2,y2 = self.pos()
        
        if (x-50 < x2 and x2 > 50+x):
            self.dy=self.dy*(-1)
            self.init_mover(dx=self.dx*self.spd+self.addDir, dy =self.dy*self.spd)
            brick.hit()
            return

        if (y-15 < y2 and y2 > 15+y ):
            self.dx=self.dx*(-1)
            self.init_mover(dx=self.dx*self.spd+self.addDir, dy =self.dy*self.spd)
            brick.hit()
            return

        self.init_mover(dx=self.dx*self.spd+self.addDir*(-1), dy =self.dy*self.spd)
        brick.hit()
        return
        
    def isInScreen(self):
        oldPos = (x,y) = self.pos()
        newDir = random.randrange(2)
        if (x < 0 + 10):
            x = 0 + 10
            if self.spd < 3:
                self.spd = self.spd + 1
            self.dx=self.dx*(-1)
            self.addDir = self.addDir*(-1)
            self.init_mover(dx=self.dx*self.spd+self.addDir, dy =self.dy*self.spd)
        if (y < 0 + 10):
            y = 0 + 10
            if self.spd < 3:
                self.spd = self.spd + 1
            self.dy=self.dy*(-1)
            self.init_mover(dx=self.dx*self.spd+self.addDir, dy =self.dy*self.spd)
        if (x > 700 - 10):
            x = 700 - 10
            if self.spd < 3:
                self.spd = self.spd + 1
            self.dx=self.dx*(-1)
            self.addDir = self.addDir*(-1)
            self.init_mover(dx=self.dx*self.spd+self.addDir, dy =self.dy*self.spd)
        if (y > 725 + 20):
            global ballCount
            ballCount = ballCount - 1
            if ballCount is 0:
                global life
                life = life - 1
                if life is 0:
                    games.Message(self.screen,725/2,725/2,"You Fail at Life",70,colour.white,25000,self.screen.quit())
                ball(self.screen)
            self.destroy()
        if oldPos is not self.pos():
            self.move_to((x,y))
    def hitSomething(self):
        for obj in self.overlapping_objects():
            if obj.isBreakable():
                self.hitBrick(obj)
    def moved(self):
        self.isInScreen()
        self.hitSomething()
# paddle
class paddle(games.Sprite,games.Mover):

    def __init__(self, screen):
        self.init_sprite(screen=screen,x=350,y=725-8,image=games.load_image('bar.bmp'))
        self.init_mover(dx=1,dy=1)

    def isInScreen(self):

        # change to keyboard
        x,y = games.pygame.mouse.get_pos()
        y = 725-8*3
        if (x < 0 + 36):
            x = 0+36
        if (x > 700 -35):
            x= 700-35
        self.move_to(x,y)

    def hitSomething(self):
        for obj in self.overlapping_objects():
            if not obj.isAItem():
                obj.hitPaddle(self.pos())
            else:
                ihetdhr = 0

    def isBreakable(self):
        return False
                
    def moved(self):
        
        # DEBUGGING
        self.isInScreen()
        self.hitSomething()
        
    
# Load from file
def loadRaw():
    default = """
1111111
1111111
1111111
2222222
3333333
"""

    # import from file later, this is for debugging
    return default

# converts raw to brick layout
def convertRaw(screen,string,images):
    
    # get rid of new lines
    string = string.replace('\n', '')

    # get rid of '*' in front
    string = string.lstrip('*')

    # '*' means the brick has an item
    itemCount = string.count('*')

    # if string is too long, cut it
    if len(string) > (7 * 8 + itemCount):
        string = string[:7 * 8 + itemCount]

    # if the string is not long enough add the least amount of ' ' needed
    if ((len(string)-itemCount) % 7) is not 0:
        string = string + ' ' * (7-((len(string)-itemCount) % 7))

    # dynamic array[n][7]
    brickArray = [[] for i in range((len(string)-itemCount)/7)]
    for row in range(len(brickArray)):
        brickArray[row] = [[] for j in range(7)]

    counter = 0
    # assign values to array, 0-9 or None. It also tells if brick drops an item.
    for row in range(len(brickArray)):
        for brck in range(7):
            if string[counter] is '*':
                try:
                    brickArray[row][brck-1].isDrop = True
                except(ValueError):
                    continue
                counter = counter + 1
            if string[counter] is not ' ':
                try:
                    brickArray[row][brck] = brick(screen, \
                                                  brck*100+50,row*30+15, \
                                                  images[int(string[counter])], \
                                                  int(string[counter]))
                except(ValueError):
                    brickArray[row][brck] = None
            else:
                brickArray[row][brck] = None
            counter = counter + 1
        
    return brickArray

# convert brick layout item to screen
def loadBricks(screen, layout, images):

    for x in range(len(layout)/7):
        for y in range(7):
            layout[x][y].load(screen, images[layout[x][y].licksToTheCenter], x*30, y*100)

# sets screen
def setupBrickScreen():
    
    # Screen size
    screen = games.Screen(700, 725)

    bg = games.load_image('Bbg.bmp',0)

    # screen BG
    #screen.set_background_colour(colour.black)
    screen.set_background(bg)

    # set mouse to not_visible
    games.pygame.mouse.set_visible(False)

    # set title
    games.pygame.display.set_caption("Bricks")

    return screen

# load images
def loadImg():
    # load images
    global brickImgs
    brickImgs = games.load_image("brick0.bmp",0), \
                       games.load_image("brick1.bmp",0), \
                       games.load_image("brick2.bmp",0), \
                       games.load_image("brick3.bmp",0), \
                       games.load_image("brick4.bmp",0), \
                       games.load_image("brick5.bmp",0), \
                       games.load_image("brick6.bmp",0), \
                       games.load_image("brick7.bmp",0), \
                       games.load_image("brick8.bmp",0), \
                       games.load_image("brick9.bmp",0)
    return brickImgs

def bricksGame():
    global life
    life = 3
    raw = loadRaw()
    screen = setupBrickScreen()
    images = loadImg()
    layout = convertRaw(screen, raw, images)
    # debug
    b = ball(screen)
    p = paddle(screen)
    # screen loop start
    screen.mainloop()

bricksGame()

