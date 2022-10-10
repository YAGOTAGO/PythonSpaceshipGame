from turtle import width
import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1600, 900))
screen.fill('purple')


#sets display variables
pygame.display.set_caption("Rocket Shooter")
pygame.display.set_icon(pygame.image.load('Images\spaceship.png'))

#help with time and set frame rate
clock = pygame.time.Clock()


class SpaceShip(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        #initiate image
        self.image = pygame.image.load('Images\spaceshipFlame.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)

        #movement var
        self.gravity = 10
        self.xCoord = 200
        self.yCoord = 100

        #initiate hitbox/rect
        self.rect = self.image.get_rect(center = (200, 100))


    def update(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom>=900:
            self.rect.bottom = 900
        

#method for event handling
def eventLoop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        


#intialize game objects
spaceship = SpaceShip()
spaceshipGroup = pygame.sprite.GroupSingle()
spaceshipGroup.add(spaceship)


#Main gameplay loop
while True:
    eventLoop()

    spaceship.update() 
    spaceshipGroup.draw(screen)

    pygame.display.update() #maintains display open
    clock.tick(60) #sets fram rate to 60



