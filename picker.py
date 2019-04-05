import pygame
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Choice:
    def __init__(self, number, text):
        self.number = number
        self.text = text

    def choose(self):
        print(self.number)


class Option(pygame.sprite.Sprite):
    def __init__(self, x, y, choice, font):
        super(Option, self).__init__()
        self.surf = pygame.Surface((200, 50))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = choice.number
        self.textsurface = font.render(choice.text, False, (0, 0, 0))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
optionFont = pygame.font.SysFont('Comic Sans MS', 25)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((0, 0, 0))

choices = [Choice(1, "nix tun"), Choice(2, "was tun"), Choice(3, "irgendwas tun")]

options = pygame.sprite.Group()
optionY = 100
choiceNumber = 0
for choice in choices:
    option = Option(100, optionY, choices[choiceNumber], optionFont)
    options.add(option)
    optionY += 75
    choiceNumber += 1

numberOfOptions = len(options.sprites())
activeOptionCounter = numberOfOptions

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(15)
    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
            elif e.key == K_DOWN:
                activeOptionCounter += 1
            elif e.key == K_UP:
                activeOptionCounter -= 1
            elif e.key == K_RETURN:
                chooseOption(activeOptionCounter % numberOfOptions + 1)
        elif e.type == QUIT:
            running = False

    screen.blit(background, (0, 0))

    for option in options:
        if activeOptionCounter % numberOfOptions + 1 is option.number:
            option.surf.fill((128, 128, 0))
        else:
            option.surf.fill((0, 128, 128))

        screen.blit(option.surf, option.rect)
        screen.blit(option.textsurface, option.rect)

    pygame.display.flip()