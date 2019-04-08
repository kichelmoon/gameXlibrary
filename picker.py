import pygame
from pygame.locals import *
import xml.dom.minidom


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
newChoiceEvent = pygame.USEREVENT + 1


class GameFile:
    def __init__(self, filepath):
        self.doc = xml.dom.minidom.parse(filepath)
        self.sets = self.doc.getElementsByTagName('set')

    def getSetByNumber(self, number):
        for element in self.sets:
            if int(element.attributes['number'].value) == int(number):
                return element.getElementsByTagName('choice')

        return None


class Choice:
    def __init__(self, number, text):
        self.number = number
        self.text = text

    def choose(self):
        pygame.event.post(pygame.event.Event(newChoiceEvent, {'newNumber': self.number}))


class GameStore:
    def __init__(self, gameFile):
        self.gameFile = gameFile

    def getChoicesByNumber(self, number):
        xmlChoices = self.gameFile.getSetByNumber(number)
        choiceList = []
        for xmlChoice in xmlChoices:
            choiceList.append(Choice(xmlChoice.attributes['next'].value, xmlChoice.childNodes[0].nodeValue))

        return choiceList


class OptionSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, choice, font, number):
        super(OptionSprite, self).__init__()
        self.surf = pygame.Surface((200, 50))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.choice = choice
        self.textsurface = font.render(choice.text, False, (0, 0, 0))
        self.number = number


def makeOptionFromChoices(choices):
    options = pygame.sprite.Group()
    optionY = 100
    choiceNumber = 0
    for choice in choices:
        option = OptionSprite(100, optionY, choices[choiceNumber], optionFont, choiceNumber + 1)
        options.add(option)
        optionY += 75
        choiceNumber += 1

    return options


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
optionFont = pygame.font.SysFont('Comic Sans MS', 25)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((0, 0, 0))

gameStore = GameStore(GameFile('choices.xml'))

choices = gameStore.getChoicesByNumber(1)

options = makeOptionFromChoices(choices)
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
                for option in options:
                    if option.number == activeOptionCounter % numberOfOptions + 1:
                        option.choice.choose()
        elif e.type == QUIT:
            running = False
        elif e.type == newChoiceEvent:
            options = makeOptionFromChoices(gameStore.getChoicesByNumber(e.newNumber))
            numberOfOptions = len(options.sprites())
            activeOptionCounter = numberOfOptions

    screen.blit(background, (0, 0))

    for option in options:
        if activeOptionCounter % numberOfOptions + 1 is option.number:
            option.surf.fill((128, 128, 0))
        else:
            option.surf.fill((0, 128, 128))

        screen.blit(option.surf, option.rect)
        screen.blit(option.textsurface, option.rect)

    pygame.display.flip()