from operator import truediv
from pickle import TRUE
from tkinter import Y
from tokenize import group
from turtle import back, width
import pygame
from sys import exit

#important vars
WIDTH = 1300
HEIGHT = 800
TOPBOUND = 70
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
UICENTERY = 40
#Action vars
shoot = False
thrustersOn = False

#Bullet
purpleBullet = pygame.image.load("Images\dripBall.png").convert_alpha()
blueBullet = pygame.image.load("Images\spaceshipBall.png").convert_alpha()
blueBulletRect = blueBullet.get_rect(center =  (380, UICENTERY))

#font
fontSize = 50
gameFont = pygame.font.Font('Fonts\AudiowideFont.ttf', fontSize)
startTime = 0

#heart
heartImg = pygame.image.load('Images\heart.png').convert_alpha()
heartRect = heartImg.get_rect(center = (100, UICENTERY))

#fuel
fuelImg = pygame.image.load('Images\FuelCanister.png').convert_alpha()
fuelRect = fuelImg.get_rect(center = (600, UICENTERY))

#Groups
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
            self.kill()
            self.alive = False
            startTime = int (pygame.time.get_ticks()/ 1000) ## when making restart game function this will be how to reset the time

        #movement
        if thrustersOn:
            self.MoveUp()

        #shoot
        if shoot:
            self.shoot()

        #decreases shot cooldown
        if self.shootCD>0:
            self.shootCD-=1

        #speed of spaceship
        self.velocity = (self.damping * self.velocity) + self.gravity
        self.rect.y += self.velocity

        #bounds spaceship
        if self.rect.bottom>= HEIGHT:
            self.rect.bottom = HEIGHT
            if self.health>0:
                self.health -=1
        elif self.rect.top <= TOPBOUND:
            self.rect.top = TOPBOUND
        
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

#spaceship
spaceship = SpaceShip()
spaceshipGroup = pygame.sprite.GroupSingle()
spaceshipGroup.add(spaceship)

#Enemies
dripDudeImg = pygame.image.load("Images\dripGuy.png").convert_alpha()
dripDude =  DripGuy(dripDudeImg, 200, 8, WIDTH -200, HEIGHT -300, 20)

EnemiesGroup = pygame.sprite.Group()
EnemiesGroup.add(dripDude)

#method for displaying the time passed
def displayInfo(x, y, info): 
    timeSurf = gameFont.render(f'{info}', False, 'White')
    timeRect = timeSurf.get_rect(center = (x,y))
    screen.blit(timeSurf, timeRect)

#method for event handling
def eventLoop():
    global thrustersOn
    global shoot

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


#Main gameplay loop
gameOver = False
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
    
    #displays health
    screen.blit(heartImg, heartRect)
    displayInfo(200, UICENTERY, spaceship.health)

    #display ammo
    screen.blit(blueBullet, blueBulletRect)
    displayInfo(445, UICENTERY, spaceship.ammo)

    #display fuel
    screen.blit(fuelImg, fuelRect)
    displayInfo(710, UICENTERY, spaceship.fuel)

    #update and draw groups

    #spaceship group
    spaceshipGroup.update() 
    spaceshipGroup.draw(screen)
    
    #enemies
    EnemiesGroup.update()
    EnemiesGroup.draw(screen)

    #bullet group
    bulletGroup.update()
    bulletGroup.draw(screen)



    pygame.display.update() #maintains display open
    clock.tick(FPS) #sets fram rate to 60



