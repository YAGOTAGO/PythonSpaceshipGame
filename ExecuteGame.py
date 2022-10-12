from pickle import TRUE
from random import randint
from tkinter import EventType
import pygame
from sys import exit

#important vars
WIDTH = 1300
HEIGHT = 800
TOPBOUND = 70
FPS = 60
UICENTERY = 40

#pygame scree
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#spawn vars
SPAWNX = WIDTH + 100
SPWANY1 = TOPBOUND+50
SPAWNY2 = HEIGHT-50
COLLECTABLESMOVESPEED = 6

#Action vars
shoot = False
thrustersOn = False

#Bullet
purpleBullet = pygame.image.load("Images\dripBall.png").convert_alpha()
blueBullet = pygame.image.load("Images\spaceshipBall.png").convert_alpha()
blueBulletRect = blueBullet.get_rect(center =  (380, UICENTERY))

#ammo
ammoAmount = 15 # amoung given when collected
ammoCD = 300 #start of game cd
maxAmmoCD = 160 # cd after first spawn
ammoImg = pygame.image.load('Images\drip.png').convert_alpha()

#font
fontSize = 50
gameFont = pygame.font.Font('Fonts\AudiowideFont.ttf', fontSize)
startTime = 0

#explosion images
explosion1 = pygame.image.load('Images\explosion\explosion1.png').convert_alpha()
explosion2 = pygame.image.load('Images\explosion\explosion2.png').convert_alpha()
explosion3 = pygame.image.load('Images\explosion\explosion3.png').convert_alpha()
explosion4 = pygame.image.load('Images\explosion\explosion4.png').convert_alpha()
explosion5 = pygame.image.load('Images\explosion\explosion5.png').convert_alpha()
explosion6 = pygame.image.load('Images\explosion\explosion6.png').convert_alpha()
explosionIndex = 0
explosionFrames = [explosion1, explosion2, explosion3, explosion4, explosion5, explosion6]
explodeOnce = True

#coins images
coin1 = pygame.image.load('Images\coins\Gold1.png').convert_alpha()
coin2 = pygame.image.load('Images\coins\Gold2.png').convert_alpha()
coin3 = pygame.image.load('Images\coins\Gold3.png').convert_alpha()
coin4 = pygame.image.load('Images\coins\Gold4.png').convert_alpha()
coin5 = pygame.image.load('Images\coins\Gold5.png').convert_alpha()
coin6 = pygame.image.load('Images\coins\Gold6.png').convert_alpha()
coin7 = pygame.image.load('Images\coins\Gold7.png').convert_alpha()
coin8 = pygame.image.load('Images\coins\Gold8.png').convert_alpha()
coin9 = pygame.image.load('Images\coins\Gold9.png').convert_alpha()
coin10 = pygame.image.load('Images\coins\Gold10.png').convert_alpha()
coin1Rect = coin1.get_rect(center = (1000, UICENTERY)) #positions coin icon for score
coinCD = 0
maxCoinCD = 40

#heart for UI
heartImg = pygame.image.load('Images\heart.png').convert_alpha()
heartRect = heartImg.get_rect(center = (100, UICENTERY))

#heart for collectible
healthRecoverAmount = 100
heartCD = 1000 #start of game cd
maxHeartCD = 700 # cd after first spawn

#fuel
fuelImg = pygame.image.load('Images\FuelCanister.png').convert_alpha()
redFuelImg = pygame.image.load('Images\Fuel.png').convert_alpha()
fuelRect = fuelImg.get_rect(center = (600, UICENTERY))
fuelRecoverAmount = 1000
fuelCD = 2000
maxFuelCd = 2000

#main menu
mainMenuImg = pygame.image.load('Images\startBackground.png').convert_alpha()

#bullet groups
bulletGroup = pygame.sprite.Group()

#sets display variables
pygame.display.set_caption("Rocket Shooter")
pygame.display.set_icon(pygame.image.load('Images\spaceship.png'))

#help with time and set frame rate
clock = pygame.time.Clock()

#background
bg = pygame.image.load('Images\Background.png').convert_alpha()
bgWidth = bg.get_width()
scroll = 0


class SpaceShip(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        #initiate image
        self.image = pygame.image.load('Images\spaceshipFlame.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        
        #health
        self.health = 500
        self.alive = True

        #shoot vars
        self.direction = 1
        self.shootCD = 0
        self.startAmmo = 50
        self.ammo = self.startAmmo

        #score/coins
        self.score = 0

        #movement var
        self.gravity = 3
        self.velocity = 0
        self.damping = .8
        self.thrust = 8
        self.fuel = 10000
        self.fuelUsage = 2

        #initiate hitbox/rect
        self.rect = self.image.get_rect(center = (200, 100))

    def update(self):
        global startTime

        if(self.health <=0):
            self.health = 0
            self.onPlayerDeath()

        #movement
        if thrustersOn:
            self.MoveUp()

        #shoot
        if shoot:
            self.shoot()

        #decreases shot cooldown
        if self.shootCD > 0:
            self.shootCD -= 1

        #speed of spaceship
        self.velocity = (self.damping * self.velocity) + self.gravity
        self.rect.y += self.velocity

        #bounds spaceship
        if self.rect.bottom>= HEIGHT:
            self.rect.bottom = HEIGHT
            if self.health>0:
                self.health -= 2 #loses health when touching the ground
        elif self.rect.top <= TOPBOUND:
            self.rect.top = TOPBOUND
        
    def onPlayerDeath(self):
        self.kill()
        self.alive = False
    
    def MoveUp(self):
        if self.fuel>=0:
            self.velocity -= self.thrust
            self.fuel -= self.fuelUsage

    def shoot(self):
        if self.shootCD == 0 and self.ammo>0:
            self.shootCD = 20
            bullet = Bullet(self.rect.right+14, self.rect.centery, self.direction, blueBullet)
            bulletGroup.add(bullet)
            self.ammo-=1
            

#end of spaceship class

#spaceship group
spaceship = SpaceShip()
spaceshipGroup = pygame.sprite.GroupSingle()
spaceshipGroup.add(spaceship)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, image):
        super().__init__()
        self.speed = 10
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self):
        self.rect.x += (self.direction * self.speed)

        #destroys excess bullets
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
        
        #check collision with characters
        if pygame.sprite.spritecollide(spaceship, bulletGroup, False):
           if(spaceship.alive):
                self.kill() #destroy bullet
                spaceship.health-= 50
                
        if pygame.sprite.spritecollide(dripDude, bulletGroup, False):
            if dripDude.alive:
                self.kill() #destroy bullet
                dripDude.health -= 50
           
#end of bullet class


class Enemy(pygame.sprite.Sprite):

    def __init__(self, image, health, speed, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.health = health
        self.speed = speed
        self.alive = TRUE
        self.direction = -1
    
    def update(self):
        #decreases shot cooldown
        if self.shootCD>0:
            self.shootCD-=1
        
        #destroys self on 0 health    
        if self.health<=0:
            self.alive = False
            self.kill()
            
           
            
class DripGuy(Enemy):

    def __init__(self, image, health, speed,x,y, shootCD):
        super().__init__(image, health, speed,x,y)
        self.goingUp = False
        self.goingDown = True
        self.shootCD = shootCD
        self.startShootcd = shootCD

    def update(self):
        
        #movement
        self.movement()

        #decreases shot cooldown
        if self.shootCD>0:
            self.shootCD-=1
        
        #destroys self on 0 health    
        if self.health<=0:
            self.alive = False
            self.kill()

        if self.alive:
            self.shoot()


    def movement(self):
        if(self.goingDown and self.rect.y < HEIGHT-100):
            self.rect.y += self.speed
        else:
            self.goingDown = False
            self.goingUp = True

        if(self.goingUp and self.rect.y > 100):
            self.rect.y -= self.speed
        else:
            self.goingDown = True
            self.goingUp = False
    

    def shoot(self):
        if self.shootCD == 0:
            self.shootCD = self.startShootcd
            bullet = Bullet(self.rect.left-15, self.rect.bottom - 40, self.direction, purpleBullet)
            bulletGroup.add(bullet)
#end of dripguy class

#coins
coinGroup = pygame.sprite.Group()

class Coin(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.frames = [coin1, coin2, coin3, coin4, coin5, coin6, coin7, coin8, coin9, coin10]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center = (SPAWNX, randint(SPWANY1, SPAWNY2))) #center off screen and random y
        self.moveSpeed = COLLECTABLESMOVESPEED
        self.animSpeed = .1
    
    def move(self):
        #destroy if off screen otherwise move it fowards
        if(self.rect.x < -100):
            self.kill()
        else:
            self.rect.x -= self.moveSpeed

    def anim(self):
        self.index += self.animSpeed
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def collide(self):
        if pygame.sprite.spritecollide(spaceship, coinGroup, True):
            spaceship.score += 100

    def update(self):
        self.collide()
        self.move()
        self.anim()


class NonAnimCollectables(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = (SPAWNX, randint(SPWANY1, SPAWNY2)))
        self.moveSpeed = COLLECTABLESMOVESPEED

    def move(self):
        #destroy if off screen otherwise move it fowards
        if(self.rect.x < -100):
            self.kill()
        else:
            self.rect.x -= self.moveSpeed
    

#ammo group
ammoGroup = pygame.sprite.Group()

class Ammo(NonAnimCollectables):

    def __init__(self, image):
        super().__init__(image)
 
    def collide(self):
        if pygame.sprite.spritecollide(spaceship, ammoGroup, True): 
            spaceship.ammo += ammoAmount

    def update(self):
        self.collide()
        self.move()


#heart group
heartGroup = pygame.sprite.Group()

class Heart(NonAnimCollectables):
    def __init__(self, image):
        super().__init__(image)
 
    def collide(self):
        if pygame.sprite.spritecollide(spaceship, heartGroup, True): 
            spaceship.health += healthRecoverAmount
    
    def update(self):
        self.collide()
        self.move()

#fuel group
fuelGroup = pygame.sprite.Group()

class Fuel(NonAnimCollectables):
    def __init__(self, image):
        super().__init__(image)
 
    def collide(self):
        if pygame.sprite.spritecollide(spaceship, fuelGroup, True): 
            spaceship.fuel += fuelRecoverAmount
    
    def update(self):
        self.collide()
        self.move()


#Enemies
dripDudeImg = pygame.image.load("Images\dripGuy.png").convert_alpha()
dripDude =  DripGuy(dripDudeImg, 200, 8, WIDTH -200, HEIGHT -300, 20)

EnemiesGroup = pygame.sprite.Group()
EnemiesGroup.add(dripDude)


#spawn collectable functions

def spawnCoin():
    global coinCD
    if coinCD == 0:
        coin = Coin()
        coinGroup.add(coin)
        coinCD = maxCoinCD
    else:
        coinCD-=1

def spawnAmmo():
    global ammoCD   
    if ammoCD == 0:
        ammo = Ammo(ammoImg)
        ammoGroup.add(ammo)
        ammoCD = maxAmmoCD
    else:
        ammoCD -= 1

def spawnHeart():
    global heartCD
    if heartCD == 0:
        heart = Heart(heartImg)
        heartGroup.add(heart)
        heartCD = maxHeartCD
    else:
        heartCD -= 1

def spawnFuel():
    global fuelCD
    if fuelCD == 0:
        fuel = Fuel(redFuelImg)
        fuelGroup.add(fuel)
        fuelCD = maxFuelCd
    else:
        fuelCD -= 1

#method for displaying the time passed
def displayInfo(x, y, info): 
    timeSurf = gameFont.render(f'{info}', False, 'White')
    timeRect = timeSurf.get_rect(center = (x,y))
    screen.blit(timeSurf, timeRect)

#method for explosion
def explosion(rect):
    global explosionIndex, explodeOnce
    
    if explodeOnce:
        if explosionIndex <= len(explosionFrames):
            screen.blit(explosionFrames[int(explosionIndex)], rect)
            explosionIndex += .2
        else:
            explosionIndex = 0
            explodeOnce = False
        

    

#method for event handling during the game
def eventLoop():
    global thrustersOn, shoot

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit logic
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # thrusters on (up key down)
                thrustersOn = True
                
            if event.key == pygame.K_SPACE: # shooting (space)
                shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP: # thrusters off (up key release)
                thrustersOn = False
            if event.key == pygame.K_SPACE: # shooting (space)
                shoot = False

#MainScreen

#Main gameplay loop
gameOver = False

def play():
    global scroll
    while not gameOver:

        eventLoop() #registers all events

        #scroll background
        for i in range(0,2):
            screen.blit(bg, (i * bgWidth + scroll, 0)) # draw background

        #reset scroll
        if abs(scroll)>bgWidth:
            scroll = 0
        scroll -= 5

        #displays information
        #displayInfo(100,40, int (pygame.time.get_ticks()/ 1000) - startTime) # displays the time in seconds
        
        #displays health UI
        screen.blit(heartImg, heartRect)
        displayInfo(200, UICENTERY, spaceship.health)

        #display ammo UI
        screen.blit(blueBullet, blueBulletRect)
        displayInfo(445, UICENTERY, spaceship.ammo)

        #display fuel UI
        screen.blit(fuelImg, fuelRect)
        displayInfo(710, UICENTERY, spaceship.fuel)

        #display score UI
        screen.blit(coin1, coin1Rect)
        displayInfo(1100, UICENTERY, spaceship.score)

        #update and draw groups

        #spaceship group
        spaceshipGroup.update() 
        spaceshipGroup.draw(screen)
        
        #coins
        spawnCoin()
        coinGroup.update()
        coinGroup.draw(screen)

        #heart
        spawnHeart()
        heartGroup.update()
        heartGroup.draw(screen)

        #spawn ammo
        spawnAmmo()
        ammoGroup.update()
        ammoGroup.draw(screen)

        #fuel
        spawnFuel()
        fuelGroup.update()
        fuelGroup.draw(screen)

        #enemies
        EnemiesGroup.update()
        EnemiesGroup.draw(screen)

        #bullet group
        bulletGroup.update()
        bulletGroup.draw(screen)

        if(spaceship.alive == False):
            explosion(spaceship.rect.topleft)

        pygame.display.update() #maintains display open
        clock.tick(FPS) #sets fram rate to 60


def mainMenu():
    while True:
        screen.blit(mainMenuImg, (0,0)) #Draws Main Menu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: #if key S is pressed then start the game
                    play()

        pygame.display.update()

mainMenu()
