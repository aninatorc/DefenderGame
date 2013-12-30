#ANN CHEN TERM PROJECT 112 - DEFENDER
import os, pygame,sys, string
import random
from pygame.locals import *
from defenderClasses import *

class Game(object):

    #inits the pygame
    def __init__(self):
        pygame.init()
        try:
            self.userName = raw_input('Enter Name: ') #to be used for high scores
            self.canPause = True
            self.screenSize = (1000,900)
            self.screen = pygame.display.set_mode(self.screenSize)
            pygame.display.set_caption("Space Defenders")
            self.background = pygame.Surface(self.screen.get_size())
            self.background = self.background.convert()
            self.loadScores() #reads scores from files
            self.initStartScreen()     
            pygame.display.flip()
        except:
            print "Quitting"
        

    #responds to mouse presses
    def mousePressed(self,event):
        (self.xc,self.yc) = pygame.mouse.get_pos()

        #deals with button clicking pre game start
        if (self.lv==0):

            if self.mode == 'main':
                self.mainClick()
            elif self.mode == 'help':
                self.helpClick()    
            elif self.mode == 'powerHelp':
                self.powerHelpClick()
            elif self.mode == 'enemyHelp':
                self.enemyHelpClick()
                
            elif self.mode == 'hiscores':
                self.hiscoresClick()
                
        #button clicking when game is over  
        else:
            if self.isGameOver == True:
                if self.restartButton.rect.collidepoint((self.xc,self.yc)):
                    self.isGameOver = False
                    self.initStartScreen()
    
    #deals with button clicking on main menu, and help screens
    def mainClick(self):
        if self.startButton.rect.collidepoint((self.xc,self.yc)):
            self.initLv()
        elif self.helpButton.rect.collidepoint((self.xc,self.yc)):
            self.initHelp()
        elif self.hiscoreButton.rect.collidepoint((self.xc,self.yc)):
            self.initHiscores()

    def helpClick(self):
        if self.backButton.rect.collidepoint((self.xc,self.yc)):
            self.initStartScreen()
        elif self.moreButton.rect.collidepoint((self.xc,self.yc)):
            self.initPowerHelp()

    def powerHelpClick(self):
        if self.backButton.rect.collidepoint((self.xc,self.yc)): 
            self.initHelp() 
        elif self.moreButton.rect.collidepoint((self.xc,self.yc)): 
            self.initEnemyHelp() 

    def enemyHelpClick(self):
        if self.backButton.rect.collidepoint((self.xc,self.yc)):
            self.initPowerHelp()
            self.buttonList.add(self.moreButton)
            self.spritesList.add(self.moreButton)

    def hiscoresClick(self):
        if self.backButton.rect.collidepoint((self.xc,self.yc)):
            self.initStartScreen()                      

    #responds to keypressed.
    def keyPressed(self,event):
        keys = pygame.key.get_pressed()
        #moves ship in response (can hold down)
        if (event.type == pygame.KEYDOWN and
            self.isGameOver ==False and self.lv !=0):
            if keys[K_LEFT]:
                self.player.rect.x -=self.player.moveX
            if keys[K_RIGHT]:
                self.player.rect.x +=self.player.moveX
            if keys[K_UP]:
                self.player.rect.y -=self.player.moveY
            if keys[K_DOWN]:
                self.player.rect.y +=self.player.moveY
            if keys[K_SPACE]: #fires missile
                self.fireMissile()
            if keys[K_p]: #pauses game
                if self.canPause:
                    self.dealWithPause()
            if keys[K_n]:
                self.nukeActivate()

            ##editor's mode
            if keys[K_q]:
                self.spawnHoming()
            if keys[K_w]:
                self.spawnShooting()
            if keys[K_e]:
                self.spawnSplitting()
            if keys[K_a]:
                self.powerLv+=1
            if keys[K_r]:
                self.lives+=1
            

    #ensures that pause doesn't unpause quickly due to speedy framerate
    def dealWithPause(self):
        if self.pause==False:
            self.pause = True
            self.drawPause()
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause() #stops sound
            self.pause = False
        self.canPause = False
        
    #initializes the help screen
    def initHelp(self):

        #loads image w/ instructions to screen
        self.mode = 'help'
        self.buttonList.remove(self.helpButton,self.startButton,self.hiscoreButton)
        self.spritesList.remove(self.startButton,self.helpButton,self.hiscoreButton)       
        self.background = load_image("instructions.png",-1)
        self.background = pygame.transform.scale(self.background,self.screenSize)

        #back to main screen button
        if len(self.buttonList) ==0:
            self.backButton = Button('back', (400,800))
            self.moreButton = Button('more', (750,800))
            self.spritesList.add(self.backButton,self.moreButton)
            self.buttonList.add(self.backButton,self.moreButton)

    #initializes the appropriate help screens
    def initPowerHelp(self):
        self.mode = 'powerHelp'
        self.background = load_image('powerhelp.png',-1)
        self.background = pygame.transform.scale(self.background,self.screenSize)

    def initEnemyHelp(self):
        self.mode = 'enemyHelp'
        self.background = load_image('enemyhelp.png',-1)
        self.background = pygame.transform.scale(self.background,self.screenSize)
        self.spritesList.remove(self.moreButton)

    #initializes high scores by reading in text file
    def initHiscores(self):

        self.backButton = Button('back', (400,800))
        font = pygame.font.Font("space age.ttf",70)
        margin = 120
        text = font.render("HIGH SCORES",1,self.turq)
        textpos = text.get_rect(centerx = self.width/2, centery= 50)
        self.screen.blit(text,textpos)
        self.mode = 'hiscores'
        self.background = load_image ('space.jpg',-1)
        lineNumber = 0
        for scorer in self.scorers:
            lineNumber +=1
            text = font.render (("%3s. %-5s %5s") %\
                                (lineNumber, scorer.name,scorer.score), \
                                1 ,self.turq)
            textpos = text.get_rect(x = 150,y =  margin*lineNumber)
            self.screen.blit(text,textpos)
        self.buttonList.empty()
        self.spritesList.empty()
        self.buttonList.add(self.backButton)
        self.spritesList.add(self.backButton)

    #inits the timers, sprites, and other data required
    def initLv(self):
        self.screen.fill((0,0,0))
        self.initTimers()
        self.buttonList.empty()
        self.spritesList.empty()
        self.initLvSprites()
        self.initMisc()
        self.bg_sound.play()

    #inits background, bullet strength, and miscellaneous data required
    def initMisc(self):
        self.background = load_image("scrollingspace.gif",-1)
        self.background = pygame.transform.scale(self.background,self.screenSize)
        self.lv +=1
        self.pauseTimer = 0
        self.threshold =10
        self.missileStr = 1
        self.isInvulnerable = False
        self.drawPower = 0
        self.shotsFired = 0
        self.replaced = False
        self.score = 0
        self.speedLv = 1
        self.delayTime = 16
        self.nukes = 1
        self.powerLv = 1
        self.y = 0
        self.y2 = -self.height+5
        #self.lives =99
        self.lives = 3
        self.isGameOver = False
        self.missileMode = 0
        self.maxEnemies = 15
        self.next = False
        self.spawnPower()
        self.spawnEnemies()

    #controls delays for powerups and shooting
    def initTimers(self):
        self.enemyFireTimer = 0
        self.enemyTimer = 0
        self.powerSpawnTimer = 250
        self.fireTimer = 4
        self.powerTimer = 0
        self.canFire = True
        self.canPause = True
        self.deathTimer = 0
        self.expTimer = 0
        self.explosionPhase = 0
        self.nukeTimer = 0

    #initializes sprite groups and lists of sprites
    def initLvSprites(self):
        
        self.enemies = [basicEnemy]                                                         
        self.prevExp = Explosion(0)                  
        self.player = Ship()
        self.spritesList.add(self.player)
        self.poweruplist = [fatMissilePower,lifePower,speedPower,nukePower,\
                            firePower]#,invinciblePower]
        self.spritesList.remove(self.helpButton,self.startButton,self.hiscoreButton)
        self.restartButton = Button('menu',(self.width/2-100,self.height/2+250))
        self.hitx = None
        self.hity = None

    def spawnHoming(self): #TEST PURPOSES
        self.enemy = homingEnemy()
        self.enemy.rect.x = random.randint(0,self.width)
        self.enemy.levelUp(self.lv)
        self.enemy.y = 0
        self.spritesList.add(self.enemy)
        self.enemyList.add(self.enemy)
    def spawnShooting(self):
        self.enemy = shootingEnemy()
        self.enemy.rect.x = random.randint(0,self.width)
        self.enemy.levelUp(self.lv)
        self.enemy.y = 0
        self.spritesList.add(self.enemy)
        self.enemyList.add(self.enemy)
                           
    def spawnSplitting(self):
        self.enemy = splitEnemy()
        self.enemy.rect.x = random.randint(0,self.width)
        self.enemy.levelUp(self.lv)
        self.enemy.y = 0
        self.spritesList.add(self.enemy)
        self.enemyList.add(self.enemy)
        
        
    #spawns powers at time intervals (only one on screen at time)
    def spawnPower(self):

        if len(self.powerUpList) < 1:
            self.powerSpawnTimer += random.randint(1,3)
            if self.powerSpawnTimer >=250:
                self.powerSpawnTimer = 0
                #spawns at random location
                self.power = self.poweruplist[random.randint\
                                              (0, len(self.poweruplist)-1)]()
               # self.power = fatMissilePower()
                self.power.rect.x = random.randint(0,self.width)
                self.power.rect.y = random.randint(0,self.height/2)
                self.spritesList.add(self.power)
                self.powerUpList.add(self.power)

    #spawns enemies with varying velocities at varying intervals
    def spawnEnemies(self):

        #controls max number of enemies on screen at once
        if len(self.enemyList) < self.maxEnemies:
            self.enemyTimer += random.randint(1,3)

            if self.enemyTimer >= 40:
                self.enemyTimer = 0
                self.enemy=self.enemies[random.randint(0,len(self.enemies)-1)]()
                             
                self.enemy.rect.x = random.randint(0,self.width)
                self.enemy.levelUp(self.lv)
                self.enemy.rect.y = 0
                self.spritesList.add(self.enemy)
                self.enemyList.add(self.enemy)

    #draws scenes        
    def redrawAll(self):
        #as long as game is not over or paused
        if (self.pause == False and self.isGameOver == False):
            self.screen.fill((0,0,0))
            #draws start screen, either help or main screen 
            if self.lv==0:
                self.drawStartScreen()
                if self.mode =='main':
                    self.drawTitleScreen()
                elif self.mode == 'help':
                    self.initHelp()
                elif self.mode == 'powerHelp':
                    self.initPowerHelp()
                elif self.mode == 'enemyHelp':
                    self.initEnemyHelp()
                elif self.mode == 'hiscores':
                    self.initHiscores()
            else: #draws the scrolling background and player data
                self.scrollBackground()
                self.drawStats()
                self.nukeTimerActivate()
                self.powerDisplayActivate()
        self.spritesList.draw(self.screen) #draws sprites
        self.canPauseTimer()
        pygame.display.flip()

    #displays lives, score, and level
    def drawStats(self):
        font = pygame.font.Font("space age.ttf",25)
        text = font.render( ("LIVES: %d") % (self.lives), 1, self.turq)
        textpos = text.get_rect(x =20,y = self.height-40)
        self.screen.blit(text,textpos)

        text = font.render (("SCORE: %d") % (self.score), 1, (self.turq))
        textpos = text.get_rect(x = 20, y = self.height -70)
        self.screen.blit(text,textpos)

        text = font.render (("LEVEL: %d") % (self.lv),1,(self.turq))
        textpos = text.get_rect(x = 20, y=  self.height - 100)
        self.screen.blit(text,textpos)

        text = font.render (("NUKES: %d") % (self.nukes),1,(self.turq))
        textpos = text.get_rect(x = self.width-210, y = self.height-40)
        self.screen.blit(text,textpos)

        text = font.render (("SPEED LV: %d") % (self.speedLv),1,(self.turq))
        textpos = text.get_rect(x = self.width-210, y= self.height-70)
        self.screen.blit(text,textpos)

        text = font.render (("POWER LV: %s") % (self.powerLv),1,(self.turq))
        textpos = text.get_rect(x = self.width -210, y = self.height -100)
        self.screen.blit(text,textpos)

    #draws background
    def drawStartScreen(self):
        self.screen.blit(self.background, (0,0))        
        self.lv = 0

    #draws main menu screen
    def drawTitleScreen(self):

        font = pygame.font.Font("space age.ttf",100)
        text = font.render (("DEFENDER"), 1 ,self.turq)
        textpos = text.get_rect(centerx = self.width/2,centery = self.height/4)
        self.background.blit(text,textpos)

        #adds main menu buttons
        if len(self.spritesList) == 0:
            self.startButton = Button('start',(200,400))
            self.helpButton = Button ('help', (300,500))
            self.hiscoreButton = Button ('hiscores', (400,600))
            self.buttonList.add(self.startButton,self.helpButton,\
                                self.hiscoreButton)
            self.spritesList.add(self.startButton,self.helpButton,\
                                 self.hiscoreButton)

    #scrolls space background
    def scrollBackground(self):

        self.y+=3
        self.y2+=3
        self.screen.blit(self.background, (0, self.y))
        self.screen.blit(self.background, (0,self.y2))
        if (self.y >=self.height):
            self.y = -self.height
        if (self.y2 >=self.height):
            self.y2 = -self.height

    #updates all of the sprites
    def levelUpdate(self):
        self.spawnEnemies()
        self.fireMissileTimer()
        self.spawnPower()
        self.checkPowerUpCollide()
        self.checkEnemyCollide()
        self.updateEnemies()
        self.enemyFire()
        self.updateShip()
        self.updatePowerUp()
        self.updateMissiles()
        self.updateEnemyMissiles()
        self.checkMissileCollide()
        self.checkEnemyMissileCollide()
        self.scoreLevelUp()


    #draws pause screen
    def drawPause(self):
        #self.screen.fill((0,0,0))

        font = pygame.font.Font("space age.ttf",80)
        text = font.render (("PAUSED"), 1 ,self.turq)
        textpos = text.get_rect(centerx = self.width/2,centery = self.height/2)
        self.screen.blit(text,textpos)
        pygame.display.update()
        pygame.display.flip()

    #runs at 20fps and updates 
    def timerFired(self):

        if self.isGameOver ==False and self.pause ==False:  
            self.clock.tick(20)
            if (self.lv !=0):
                self.levelUpdate()
        self.redrawAll()
        #handles events

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mousePressed(event)
            elif (event.type == pygame.KEYDOWN):
                self.keyPressed(event)
        pygame.display.flip()

    #loads high scores stored in text file
    def loadScores(self):
        self.scorers = []
        try:
            with open('scores.txt', "r") as f:
                lineNumber = 0

                for line in f:
                    line = line.replace("\n","")

                    blank = line.find(" ")
                    name = line[0:blank]
                    
                    score = line[blank+1:]
                    self.scorers.append(Scorer(name,score))
        except IOError as e:
            print "High Score file not found"
        
    #initializes the start screen
    def initStartScreen(self):
        self.mode = 'main'
        self.background = load_image("space2.jpg",-1)
        self.background=pygame.transform.scale(self.background,self.screenSize)
        self.clock = pygame.time.Clock()
        self.powerClock = pygame.time.Clock()
        self.lv = 0
        self.width = self.background.get_width()
        self.height = self.background.get_height()

        #inits enemy sprites groups
        self.spritesList = pygame.sprite.Group()
        self.missileList = pygame.sprite.Group()
        self.enemyMissileList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.powerUpList = pygame.sprite.Group()
        self.buttonList = pygame.sprite.Group()

    #updates enemy movement
    def updateEnemies(self):

        for enemy in self.enemyList:
            if isinstance(enemy,homingEnemy): #homingEnemy
                enemy.updatePos(self.player.rect.x,self.player.rect.y)

            #moves each enemy by determined velocity
            enemy.rect.x += enemy.moveX
            enemy.rect.y += enemy.moveY

            if isinstance(self.enemy,diagEnemy):#diag wraps around
                enemy.rect.x%=self.width
                enemy.rect.y%=self.height
            
            else:
                #removes enemy if goes off the screen
                if (enemy.rect.y >= self.height or
                    enemy.rect.x >=self.width):

                    enemy.kill()  
                    
    #allow self to wrap around
    def updateShip(self):
        self.player.rect.x %= self.width
        self.player.rect.y %=self.height

    def levelUp(self,lv):
        self.moveY+=random.randint(0,lv*5 - 5) 

    #delays player shots so they can't be OP
    def fireMissileTimer(self):
        if self.canFire == False:
            self.fireTimer +=1
            if (self.fireTimer >= self.delayTime):
                self.fireTimer = 0
                self.canFire = True
    #delays pausing so isn't annoying
    def canPauseTimer(self):

        if self.canPause == False:
            self.pauseTimer +=1
            if self.pauseTimer == 20:
                self.pauseTimer = 0
                self.canPause = True

    #fires your missile differently based on your power level    
    def fireMissile(self):

        if (self.canFire ==True):
            self.shoot_sound.play()
            if self.powerLv == 1:
                self.mainMissile()  
            elif self.powerLv == 2:
                self.mainMissile()
                self.sideMissiles(15)  
            elif self.powerLv ==3:  
                self.twoMainMissiles()
                self.sideMissiles(15)
            elif self.powerLv ==4:
                self.mainMissile()
                self.sideMissiles(15)
                self.twoMainMissiles()
            else: 
                self.mainMissile()
                self.sideMissiles(15)
                self.sideMissiles(30)
                self.twoMainMissiles()
                
            self.canFire = False

    #makes center missile
    def mainMissile(self):
        self.missile = Missile(self.missileMode)
        self.missile.rect.centerx = self.player.rect.x + self.player.width/2
        self.missile.rect.y = self.player.rect.y - self.player.height
        self.spritesList.add(self.missile)
        self.missileList.add(self.missile)

    #diagonally traveling missiles
    def sideMissiles(self,angle):
        self.missile = diagMissile(self.missileMode,angle)
        self.missile.rect.centerx = self.player.rect.x
        self.missile.rect.y = self.player.rect.y - self.player.height

        self.missile2 = backDiagMissile(self.missileMode,-angle)
        self.missile2.rect.centerx = self.player.rect.x + self.player.width
        self.missile2.rect.y = self.player.rect.y - self.player.height

        self.spritesList.add(self.missile,self.missile2)
        self.missileList.add(self.missile,self.missile2)

    #center 2 missiles
    def twoMainMissiles(self):
        self.missile = Missile(self.missileMode)
        self.missile.rect.centerx = self.player.rect.centerx + self.player.width/4
        self.missile.rect.y = self.player.rect.y - self.player.height

        self.missile2 = Missile(self.missileMode)
        self.missile2.rect.centerx = self.player.rect.centerx - self.player.width/4
        self.missile2.rect.y = self.missile.rect.y

        self.spritesList.add(self.missile,self.missile2)
        self.missileList.add(self.missile,self.missile2)

    #enemy fires at YOU at random intervals 
    def enemyFire(self):

        self.enemyFireTimer += random.randint(1,3)
        if self.enemyFireTimer >= 30:
            self.enemyFireTimer = 0
            self.fireEnemyMissile()

    #fires the enemy missiles
    def fireEnemyMissile(self):

        for enemy in self.enemyList:
            if isinstance(enemy,shootingEnemy):

                self.missile = enemyMissile()
                self.missile.rect.x = enemy.rect.x + enemy.width/2
                self.missile.rect.y = enemy.rect.y + enemy.height
                self.spritesList.add(self.missile)
                self.enemyMissileList.add(self.missile)

    #updates the enemy missiles
    def updateEnemyMissiles(self):
        for missile in self.enemyMissileList:
            missile.rect.y +=missile.missileVelY
            if (missile.rect.y > self.height):
                self.enemyMissileList.remove(missile)
                self.spritesList.remove(missile)

    #updates the player missiles
    def updateMissiles(self):
        for missile in self.missileList:
            if type(missile) == Missile:
                missile.rect.y -=missile.missileVelY
            elif type(missile) == diagMissile or type(missile)== backDiagMissile:
                missile.rect.y -=missile.missileVelY
                missile.rect.x -= missile.missileVelX

            if (missile.rect.y <0):
                self.missileList.remove(missile)
                self.spritesList.remove(missile)

    #updates powerups (Scrolls w/ bckground)
    def updatePowerUp(self):
        self.power.rect.y +=3
        if (self.power.rect.y > self.height):
            self.powerUpList.remove(self.power)
            self.spritesList.remove(self.power)

    def gameOver(self):
        #draws game over, including score and restart button
        self.screen.fill((0,0,0))
        pygame.mixer.fadeout(2000)
        self.isGameOver = True
        self.spritesList.empty()
        font = pygame.font.Font("space age.ttf",100)
        text = font.render (("GAME OVER"), 1 ,self.turq)
        textpos = text.get_rect(centerx = self.width/2,centery = self.height/2)
        self.screen.blit(text,textpos)
        text = font.render ( ("SCORE: %d") % (self.score),1,self.turq)
        textpos = text.get_rect(centerx = self.width/2, centery= self.height/2 + 100)
        self.screen.blit(text,textpos)
        self.buttonList.add(self.restartButton)
        self.spritesList.add(self.restartButton)
        pygame.display.update()
        pygame.display.flip()
        self.checkHiscore()

    #checks to see if your score is in the top 3. if so, update the file !
    def checkHiscore(self):
        place = 0
        toWrite = ""
        for scorer in self.scorers:
            if self.replaced == False and self.score > int(scorer.score):
                self.replaced = True
                self.scorers.pop()

                self.scorers.insert(place,Scorer(self.userName,self.score))
            place+=1
        for scorer in self.scorers:
            try:
                
                f = open('scores.txt',"w")
                toWrite+=( ("%s %s\n") % (scorer.name,scorer.score))
                f.write(toWrite)
            except IOError as e:
                print "High score file not found"
         
    #if enemy collides with player, player loses life
    def checkEnemyCollide(self):
        for enemy in self.enemyList:
            hit = pygame.sprite.collide_rect(enemy,self.player)
            if (hit==True and self.isInvulnerable ==False):
                self.spritesList.remove(enemy)
                self.enemyList.remove(enemy)
                self.lives-=1
                self.deathTimer = 1

                if self.lives == 0:
                    self.gameOver()

        self.deathTimerActivate()

    #reacts to powerups
    def checkPowerUpCollide(self):
        for power in self.powerUpList:
            blocksHit = pygame.sprite.spritecollide(self.player,self.powerUpList,True)
            if (blocksHit!=[]):
                self.spritesList.remove(self.power)
                self.powerUpList.remove(self.power)

                if isinstance(self.power,fatMissilePower):
                    self.fatMissileActivate()

                elif isinstance(self.power,lifePower):
                    self.lifePowerActivate()
                    
                elif isinstance(self.power,speedPower):
                    self.speedPowerActivate()
                    
                elif isinstance(self.power,nukePower):
                    self.nukes+=1
                    
                elif isinstance(self.power,firePower):
                    self.firePowerActivate()
                self.drawPower = 1
                self.powerDisplayed = True
        self.powerTimerActivate()

    #activates your speed power (movement and shooting)
    def speedPowerActivate(self):

        if self.speedLv < 5:
            self.player.moveX +=3
            self.player.moveY +=3
            self.speedLv +=1
            self.delayTime-=3

    #gives you big bullets for some amount of timesp
    def fatMissileActivate(self):
        self.player.image = load_image('ship3.png',-1)
        self.missileStr= 5
        self.missileMode = 1
        self.powerTimer = 1

    #controls temporary time
    def powerTimerActivate(self):

        if self.powerTimer > 0:
            self.powerTimer +=1
            if self.powerTimer >= 200:
                self.powerTimer = 0
                
                self.missileMode = 0
                self.missileStr=1
                self.player.image = load_image ('ship.png',-1)

    #grants life
    def lifePowerActivate(self):
        if self.lives < 5:
            self.lives+=1
            
    #fire power level up!
    def firePowerActivate(self):
        if self.powerLv <5:
            self.powerLv +=1

    #activates your nuke! kills all enemies on screen
    def nukeActivate(self):
        
        if (self.nukes > 0):
            for enemy in self.enemyList:
                self.score+=1
                enemy.kill()
            for missile in self.enemyMissileList:
                missile.kill()
            self.bomb_sound.play()
            self.nukes-=1
            self.nukeTimer = 1

    #screen effect temporarily            
    def nukeTimerActivate(self):
        if self.nukeTimer > 0:
            self.screen.fill((255,255,255))
            self.nukeTimer +=1
            if (self.nukeTimer ==20):
                self.nukeTimer = 0

    #shows what power up you get when you ge tit
    def powerDisplayActivate(self):
        if self.drawPower > 0:
            self.drawPower +=1
            font = pygame.font.Font("space age.ttf",50)
            text = font.render (("GOT %s") % (self.power.name), 1 ,self.turq)
            textpos = text.get_rect(centerx = self.width/2,centery = self.height/2)
            self.screen.blit(text,textpos)
            if self.drawPower >=40:
                self.drawPower = 0

    #controls only displaying the message temporarily
    def drawPowerMessage(self):
        if self.drawPower > 0:
            self.drawPower+=1
            font = pygame.font.Font("space age.ttf",50)
            text = font.render (("GOT %s") % (self.power.name), 1 ,self.turq)
            textpos = text.get_rect(centerx = self.width/2,centery = self.height/2)
            self.screen.fill((0,0,0))
 
            if self.drawPower >= 20:
                self.drawPower =0
                self.powerDisplayed = False
               
    #temporarily invincible right after losing a life              
    def deathTimerActivate(self):
        if self.deathTimer > 0:
            self.isInvulnerable = True
            self.deathTimer+=1
            self.player.image = load_image('ship2.png',-1)

        if self.deathTimer ==50:
            self.isInvulnerable = False
            self.deathTimer = 0
            self.player.image = load_image('ship.png',-1)

    #checks if your missiles hit the enemies
    #structure semi adapted from veronica's space invaders
    def checkMissileCollide(self):
        for missile in self.missileList:
            blocksHit = pygame.sprite.spritecollide(missile,self.enemyList, False)
            if (blocksHit!=[]):
                self.missileList.remove(missile)
                self.spritesList.remove(missile)
            for enemy in blocksHit: #increments score based on type of enemy
                enemy.hp -= self.missileStr
                if enemy.hp <= 0:
                    if (type(enemy) == basicEnemy):
                        self.score+=1
                    elif isinstance (enemy,diagEnemy):
                        self.score+=2
                    elif isinstance(enemy,homingEnemy):
                        self.score+=3
                    elif isinstance(enemy,shootingEnemy):
                        self.score+=4
                    elif isinstance(enemy,splitEnemy):
                        self.score+=1
                        self.enemySplit(enemy)
                    self.spritesList.remove(enemy)
                    self.enemyList.remove(enemy)
                    self.hitx = enemy.rect.x
                    self.hity = enemy.rect.y
                    self.next = True
                    self.boom.play()

        self.cycleExplosion(self.hitx,self.hity) #triggers explosion animation

    #splits a splitting enemy into 2 half sized ones
    def enemySplit(self,enemy):

        origEnemy = splitEnemy()
        #determines how many times the enemy has already split
        level = origEnemy.width / enemy.width

        if level < 5: #so it doesn't split forever
            #creates 2 new enemies of the same kind
            part = splitEnemy()
            part.halve(level)
            part.rect.x = enemy.rect.x
            part.rect.y = enemy.rect.y + enemy.height

            part2 = splitEnemy()
            part2.halve(level)
            part2.rect.x = enemy.rect.x + enemy.width
            part2.rect.y = enemy.rect.y + enemy.height
            
            self.spritesList.add(part,part2)
            self.enemyList.add(part,part2)

    #levels up if score reaches certain threshold
    def scoreLevelUp(self):
        if (self.score >= self.threshold):
            self.threshold += self.score 
            self.lv+=1
            self.maxEnemies += 5
            self.enemyTimer -=3
            
            if self.lv ==2:
                self.enemies.append(diagEnemy)
            elif self.lv ==3:
                self.enemies.append(homingEnemy)
            elif self.lv == 4:
                self.enemies.append(shootingEnemy)
            elif self.lv == 5:
                self.enemies.append(splitEnemy)

    #cycles frame by frame through explosion animation
    def cycleExplosion(self,x,y):
        self.spritesList.remove(self.prevExp)
        if self.next == True:
            self.expTimer +=1
            if (self.expTimer == 1):
                self.expTimer = 0
                self.drawExplosion(x,y)
                self.explosionPhase+=1
                
    #draws the explosion briefly     
    def drawExplosion(self,x,y):

        self.spritesList.remove(self.prevExp)
        explosion = Explosion(self.explosionPhase)
        explosion.rect.x = x
        explosion.rect.y = y
        self.spritesList.add(explosion)
        self.prevExp = explosion

        if self.explosionPhase == 2:

            self.next = False
            self.explosionPhase = -1

    #checks if the enemies missiles hit YOU      
    def checkEnemyMissileCollide(self):
        for missile in self.enemyMissileList:

            hit = pygame.sprite.collide_rect(missile,self.player)
            if (hit==True and self.isInvulnerable ==False):
                self.spritesList.remove(missile)
                self.enemyMissileList.remove(missile)
                self.lives-=1
                self.deathTimer = 1

                if self.lives == 0:
                    self.gameOver()

        self.deathTimerActivate()

    #initializes the sounds used 
    def initsounds(self):
        self.bg_sound = load_sound('vision.wav')
        self.bg_sound.set_volume(.3)
        self.shoot_sound = load_sound('laser.wav')
        self.boom = load_sound('boom.wav')
        self.shoot_sound.set_volume(.5)
        self.boom.set_volume(.5)
        self.bomb_sound = load_sound('bomb.wav')

#loading images and sounds
#http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html       
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

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = name
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

def run(self):
    pygame.init()
    self.pause = False
    self.isInvulnerable = False
    self.isGameOver = False
    self.turq = (0,255,239)
    self.initsounds()
    
    pygame.key.set_repeat(1,1)

    while True:
        game.timerFired()
    

game = Game()
run(game)
