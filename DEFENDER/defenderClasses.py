#ANN CHEN TERM PROJECT 112 CLASSES
import os, pygame,sys,math
import random
from pygame.locals import *
#missile class for your missiles
class Missile(pygame.sprite.Sprite):
    def __init__(self,mode):
        pygame.sprite.Sprite.__init__(self)
        self.missileH = 30
        self.missileW = 2
        self.image = load_image('missile.png',-1)

        if (mode ==1):
           self.image = pygame.transform.scale2x(self.image)

        self.rect = self.image.get_rect()
        self.missileVelY = 40
#missiles fired at an angle
class diagMissile(Missile):
    def __init__(self,mode,orientation):
        super (diagMissile,self).__init__(mode)
        self.missileVelX = 10 * (orientation /15)
        self.center = self.rect.center

        self.original = self.image
        self.image = pygame.transform.rotate(self.original, orientation)
        self.rect = self.image.get_rect(center=self.center)
#at an angle and go the opposite direction of the normal diagMissiles
class backDiagMissile(diagMissile):
    def __init__(self,mode,orientation):
        super(backDiagMissile,self).__init__(mode,orientation)
        self.missileVelX = 10 * (orientation/15)

#enemy missiles travel slower and are smaller
class enemyMissile(Missile):
    def __init__(self, mode = 0):
        super (enemyMissile,self).__init__(self)
        self.image = load_image('enemymissile.png',-1)
        self.rect = self.image.get_rect()
        self.missileVelY = 20
#the player you control
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('ship.png',-1)
        self.rect = self.image.get_rect()
         
        self.moveX = 10
        self.moveY = 10
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.isInvulnerable = False
        self.rect.x = 1300/2
        self.rect.y = 650

#basic enemy moves in a straight line down
class basicEnemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('enemy.gif',-1)

        self.height = self.image.get_height()
        self.width = self.image.get_width()
        #self.image = pygame.Surface([width,height])
        self.rect = self.image.get_rect()
        self.moveY = random.randint(5,10)
        self.moveX = 0
        self.hp = 1

    #increases the speed of the enemy per level
    def levelUp(self,lv):
        self.moveY+=random.randint(0,lv*3)

#moves diagonally and wraps around
class diagEnemy(basicEnemy):
    def __init__(self):
        super (diagEnemy,self).__init__()
        self.moveY = random.randint(5,10)
        self.moveX = random.randint(-10,10)
        self.image = load_image('enemy2.gif',-1)
        self.rect = self.image.get_rect()
        self.hp = 2

#moves towards the player (not vertically)
class homingEnemy(basicEnemy):
    def __init__(self):
        super (homingEnemy,self).__init__()
        self.moveY = random.randint(5,10)
        self.moveX = 0
        self.moveYStore =self.moveY
        self.image = load_image('enemy3.gif',-1)
        self.rect = self.image.get_rect()
        self.hp = 2

    #updates direction based on where the player is
    def updatePos(self,px,py):

        if self.rect.x > px:
            self.moveX = -5
        elif self.rect.x < px: 
            self.moveX = 5
         
        if abs(self.rect.x - px) < 25:
            self.moveX = 0
#shoots back at you! moves the same as diag enemy
class shootingEnemy(diagEnemy):
    def __init__(self):
        super (shootingEnemy,self).__init__()
        self.image = load_image ('enemy4.gif',-1)
        self.width = self.image.get_width()
        
        self.hp = 3
#splits into 2 smaller enemies when hit
class splitEnemy(basicEnemy):
    def __init__(self):
        super (splitEnemy,self).__init__()

        self.image = load_image ('splitship.gif',-1)
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.origrect= self.rect
        self.moveY = 5   
        self.hp = 1

    #halves number of times based on how many times hit already
    def halve(self,level):
        
        self.original = self.image
        halveNum = 2 ** level # number of times to halve
        self.image = pygame.transform.scale(self.original, \
                                            (self.width/halveNum,\
                                             self.height/halveNum))
        self.rect = self.image.get_rect()

        self.width =self.width/(halveNum)
        self.height=self.height/(halveNum)
    
    
#the explosion pictures to be cycled through
class Explosion (pygame.sprite.Sprite):
    def __init__(self,phase):
        pygame.sprite.Sprite.__init__(self)
        self.explosions = [load_image('exp1.png',-1),load_image('exp2.png',-1),\
                           load_image('exp3.png',-1)]
        self.image = self.explosions[phase]
        self.rect = self.image.get_rect()      

#buttons! text blitted directly on buttons
class Button(pygame.sprite.Sprite):
    def __init__(self,buttonText,topleft,color = (0,255,239)):
        pygame.sprite.Sprite.__init__(self)
       # self.text = buttonText
        self.color = color
        self.topleft = topleft
        self.image = pygame.Surface((200,50))
        self.image.fill(self.color)
        self.image.set_alpha(130)
        self.rect = self.image.get_rect()
        self.rect.left = topleft[0]
        self.rect.top = topleft[1]
        font = pygame.font.Font("space age.ttf",30)
        text = font.render(buttonText, 1, (0,0,0))
        textpos = text.get_rect(centerx=100,centery=25)
        self.image.blit(text,textpos)

#powerups
class powerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#powerful missiles powerup sprite
class fatMissilePower(powerUp):

    def __init__(self):
        super(fatMissilePower,self).__init__()
        self.image = load_image('shootpower.png',-1)
        self.rect = self.image.get_rect()

        self.name = 'missile power'
#life++ sprite
class lifePower(powerUp):
    def __init__(self):
        super(lifePower,self).__init__()
        self.image = load_image('lifepower.png',-1)
        self.rect = self.image.get_rect()
        self.name = "life power"
    
#speed ++ sprite
class speedPower(powerUp):
    def __init__(self):
        super(speedPower,self).__init__()
        self.image = load_image('speedpower.png',-1)
        self.rect = self.image.get_rect()
        self.name = 'speed power'

#nuke sprite
class nukePower(powerUp):
    def __init__(self):
        super (nukePower,self).__init__()
        self.image = load_image('nukepower.png',-1)
        self.rect = self.image.get_rect()
        self.name = 'nuke power'

#firePower sprite
class firePower(powerUp):
    def __init__(self):
        super (firePower,self).__init__()
        #self.image.fill((255,140,0))
        self.image = load_image('firepower.png',-1)
        self.rect = self.image.get_rect()
        self.name = 'fire power'

#stores name and score of high scorers
class Scorer(object):
    def __init__(self,name,score):
        self.name = name
        self.score = score

#adapted from chimp tutorial as well
def load_image(name, colorkey=None):
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

