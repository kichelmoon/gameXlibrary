import pygame
from pygame.locals import *
import xml.dom.minidom


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class GameFile:
    def __init__(self, filepath):
        self.doc = xml.dom.minidom.parse(filepath)
        self.sets = self.doc.getElementsByTagName('set')

    def getSetByNumber(self, number):
        for element in self.sets:
            if int(element.attributes['number'].value) == number:
                return element.getElementsByTagName('choice')

        return None


class Choice:
    def __init__(self, number, text):
        self.number = number
        self.text = text

    def choose(self):
        print(self.number)


class GameStore:
    def __init__(self, gameFile):
        self.gameFile = gameFile

    def getChoicesByNumber(self, number):
        xmlChoices = self.gameFile.getSetByNumber(number)
        choiceList = []
        i = 1
        for xmlChoice in xmlChoices:
            print(xmlChoice.childNodes)
            choiceList.append(Choice(i, xmlChoice.childNodes[0].nodeValue))
            i += 1

        return choiceList


class OptionSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, choice, font):
        super(OptionSprite, self).__init__()
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

gameStore = GameStore(GameFile('choices.xml'))

choices = gameStore.getChoicesByNumber(1)

options = pygame.sprite.Group()
optionY = 100
choiceNumber = 0
for choice in choices:
    option = OptionSprite(100, optionY, choices[choiceNumber], optionFont)
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
                choices[activeOptionCounter % numberOfOptions].choose()
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