import pygame
from Cards.Card import Suit, Rank
from States.Core.StateClass import State
from States.GameState import HAND_SCORES

class RunInfoState(State):
    def __init__(self, hand,nextState: str = ""):
        super().__init__(nextState)

        self.stackSurface = pygame.Surface((900, 600), pygame.SRCALPHA)
        self.tvOverlay = pygame.image.load('Graphics/Backgrounds/CRT.png').convert_alpha()
        self.tvOverlay = pygame.transform.scale(self.tvOverlay, (1300, 750))
        self.desc = ''
        self.cards = []
        self.handNames = hand

        # default rectangle dimensions
        self.rectWidth = 500
        self.rectHeight = 30
        self.x = 350
        self.yStart = 100
        self.gap = 10
        self.font = pygame.font.Font("Graphics/Text/m6x11.ttf", 24)
        self.cardImages = State.deckManager.load_card_images()

        # labels dictionary (10)
        self.labels = {
            "Straight Flush": [100, 8, 0, 1],  # [chips,multiplier,counter,hand lvl,]
            "Four of a Kind": [60, 7, 0, 1],
            "Full House": [40, 4, 0, 1],
            "Flush": [35, 4, 0, 1],
            "Straight": [30, 4, 0, 1],
            "Three of a Kind": [30, 3, 0, 1],
            "Two Pair": [20, 2, 0, 1],
            "One Pair": [10, 2, 0, 1],
            "High Card": [5, 1, 0, 1],
            "Back": []
        }
        # descriptions for each playable hand
        self.handDescriptions = [
            "5 Cards in a row (consecutive ranks) all sharing the same suit.",
            "4 Cards with the same rank.",
            "3 Cards sharing a rank and 2 other ones sharing another rank.",
            "5 Cards that share the same suit.",
            "5 Cards in a row (consecutive ranks).",
            "3 Cards sharing a rank.",
            "2 pairs of Cards with different ranks.",
            "1 pair of Cards with the same rank",
            "If the played hand is not on the list, only the highest rank scores",
            "return to game"
        ]
        # hardcoded visual examples of hands
        self.exampleHands = [

            [(Rank.TEN, Suit.HEARTS), (Rank.JACK, Suit.HEARTS), (Rank.QUEEN, Suit.HEARTS),
             (Rank.KING, Suit.HEARTS), (Rank.ACE, Suit.HEARTS)],

            [(Rank.NINE, Suit.SPADES), (Rank.NINE, Suit.HEARTS), (Rank.NINE, Suit.DIAMONDS),
             (Rank.NINE, Suit.CLUBS), (Rank.FIVE, Suit.HEARTS)],

            [(Rank.TEN, Suit.SPADES), (Rank.TEN, Suit.HEARTS), (Rank.TEN, Suit.DIAMONDS),
             (Rank.KING, Suit.CLUBS), (Rank.KING, Suit.HEARTS)],

            [(Rank.TWO, Suit.HEARTS), (Rank.FIVE, Suit.HEARTS), (Rank.EIGHT, Suit.HEARTS),
             (Rank.JACK, Suit.HEARTS), (Rank.KING, Suit.HEARTS)],

            [(Rank.FIVE, Suit.SPADES), (Rank.SIX, Suit.HEARTS), (Rank.SEVEN, Suit.DIAMONDS),
             (Rank.EIGHT, Suit.CLUBS), (Rank.NINE, Suit.SPADES)],

            [(Rank.QUEEN, Suit.SPADES), (Rank.QUEEN, Suit.HEARTS), (Rank.QUEEN, Suit.DIAMONDS),
             (Rank.FOUR, Suit.CLUBS), (Rank.SEVEN, Suit.SPADES)],

            [(Rank.EIGHT, Suit.SPADES), (Rank.EIGHT, Suit.DIAMONDS), (Rank.FIVE, Suit.CLUBS),
             (Rank.FIVE, Suit.HEARTS), (Rank.THREE, Suit.SPADES)],

            [(Rank.JACK, Suit.HEARTS), (Rank.JACK, Suit.CLUBS), (Rank.FIVE, Suit.DIAMONDS),
             (Rank.EIGHT, Suit.SPADES), (Rank.NINE, Suit.CLUBS)],

            [(Rank.TWO, Suit.HEARTS), (Rank.FIVE, Suit.CLUBS), (Rank.SEVEN, Suit.DIAMONDS),
             (Rank.NINE, Suit.HEARTS), (Rank.KING, Suit.CLUBS)],

            []
        ]

        self.labelKeys = list(self.labels.keys())

        # create rectangles
        self.rects = []
        for i in range(10):
            if i == 9:
                gap = 15
            else:
                gap = 10
            rectY = self.yStart + i * (self.rectHeight + gap)
            rect = pygame.Rect(self.x, rectY, self.rectWidth, self.rectHeight)
            self.rects.append(rect)

    def update(self):
        self.draw()
        self.updateHandInfo()

    def updateHandInfo(self):
        # updating counter for played hand
        for i in range(len(self.handNames)):
            if self.handNames[i] in self.labelKeys:
                self.labels[self.handNames[i]][2] += 1
        self.handNames = ['']

        # leveling up logic
        for hand in HAND_SCORES:
            for key in self.labelKeys:
                if key == hand:
                    if HAND_SCORES[hand]['chips'] != self.labels[hand][0]:
                        self.labels[key][-1] = HAND_SCORES[key]["level"]
                        self.labels[key][0] = HAND_SCORES[key]["chips"]
                        self.labels[key][1] = HAND_SCORES[key]["multiplier"]

    def draw(self):
        self.screen.blit(State.screenshot, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        self.stackSurface.fill((0, 0, 0, 0))
        infoBox = pygame.Surface((400,250), pygame.SRCALPHA)
        infoBox.fill((220, 220, 220, 255))

        # Fixed offsets for clean display
        offsetLvl = 10
        offsetText = 120
        offsetChipsMult = 300
        offsetCount = 450

        for i, rect in enumerate(self.rects):
            # Hover detection
            if rect.collidepoint(pygame.mouse.get_pos()):
                if self.rects[i].collidepoint(pygame.mouse.get_pos()):
                    self.desc = self.handDescriptions[i]
                    self.cards = self.exampleHands[i]
                if self.rects[-1].collidepoint(pygame.mouse.get_pos()):
                    fillColor = (255, 0, 0)
                else:
                    fillColor = (180, 220, 255)
            else:
                fillColor = (220, 220, 220)

            pygame.draw.rect(self.stackSurface, fillColor, rect)
            pygame.draw.rect(self.stackSurface, (0, 0, 0), rect, 2)

            key = self.labelKeys[i]
            value = self.labels[key]

            # needed since back key value is empty
            if not value:
                textSurface = self.font.render(key, True, (0, 0, 0))
                textCenter = textSurface.get_rect(center=rect.center)
                self.stackSurface.blit(textSurface, textCenter)
                continue

            # Separate the values for display
            lvl = value[-1]
            count = value[2]
            chipsMult = value[:2]

            # 1. Lvl
            lvlDisp = self.font.render(f"Lvl {lvl}", True, (0, 0, 0))
            lvlRect = lvlDisp.get_rect()
            lvlRect.centery = rect.centery
            lvlRect.left = rect.left + offsetLvl
            self.stackSurface.blit(lvlDisp, lvlRect)

            # 2. hand
            textDisp = self.font.render(key, True, (0, 0, 0))
            textRect = textDisp.get_rect()
            textRect.centery = rect.centery
            textRect.left = rect.left + offsetText
            self.stackSurface.blit(textDisp, textRect)

            # 3. chips & multiplier
            chipsMultStr = " x ".join(str(v) for v in chipsMult)
            chipsMultDisp = self.font.render(chipsMultStr, True, (0, 0, 0))
            chipsMultRect = chipsMultDisp.get_rect()
            chipsMultRect.centery = rect.centery
            chipsMultRect.left = rect.left + offsetChipsMult
            self.stackSurface.blit(chipsMultDisp, chipsMultRect)

            # 4. times played counter
            countDisp = self.font.render(f"#{count}", True, (0, 0, 0))
            countRect = countDisp.get_rect()
            countRect.centery = rect.centery
            countRect.left = rect.left + offsetCount
            self.stackSurface.blit(countDisp, countRect)

            #spliting longer strings
            if self.desc:
                if len(self.desc) > 33:
                    mid = len(self.desc) // 2
                    firstHalf = self.desc[:mid]
                    secondHalf = self.desc[mid:]

                    if " " in secondHalf:
                        firstHalf = self.desc[:self.desc.rfind(" ", 0, mid)]
                        secondHalf = self.desc[len(firstHalf):].lstrip()
                    lines = [firstHalf, secondHalf]
                else:
                    lines = [self.desc]

                # Render and display each line
                strPosition = 5
                for line in lines:

                    descDisp = self.font.render(line, True, (0, 0, 0))
                    descRect = descDisp.get_rect()
                    descRect.left = 10
                    descRect.top = strPosition
                    infoBox.blit(descDisp, descRect)
                    strPosition += descRect.height + 5

            if self.cards:

                cardSize  = 55
                spacing = 20
                cardX = 10
                cardY = infoBox.get_rect().centery

                for rank, suit in self.cards:
                    img = self.cardImages.get((suit, rank))
                    if img:
                        infoBox.blit(img, (cardX, cardY))
                        cardX += cardSize + spacing

        self.screen.blit(self.stackSurface, (0, 0))
        self.screen.blit(infoBox, (850, 200))
        self.screen.blit(self.tvOverlay,(0,0))

    """ Handle user input """
    def userInput(self, events):
        if events.type == pygame.QUIT:
            self.isFinished = True
            self.nextState = "GameState"

        elif events.type == pygame.MOUSEBUTTONDOWN:
            if self.rects[-1].collidepoint(events.pos):
                self.isFinished = True
                self.nextState = "GameState"
            else:
                self.isFinished = False
