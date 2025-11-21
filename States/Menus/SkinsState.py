import pygame
import Deck.DeckManager
from States.Core.StateClass import State

class SkinsState(State):
    def __init__(self, nextState: str = ""):
        super().__init__(nextState)

        #Background
        self.backgroundImage = pygame.image.load('Graphics/Backgrounds/introBackground.jpeg')
        self.background = pygame.transform.scale(self.backgroundImage, (1300, 750))
        self.backgroundRect = self.background.get_rect(topleft=(0, 0))

        # --- CRT overlay ---
        self.tvOverlay_raw = pygame.image.load('Graphics/backgrounds/CRT.png').convert_alpha()
        self.buy_sound = pygame.mixer.Sound("Graphics/Sounds/buySFX.wav")
        self.buy_sound.set_volume(1.0)
        self.tvOverlay = pygame.transform.scale(self.tvOverlay_raw, (1300, 750))
        self.tvOverlay.set_alpha(160)

        # --- Fonts ---
        self.font = pygame.font.Font("graphics/Text/m6x11.ttf", 30)
        self.titleText = self.font.render("Select Your Skin", True, 'white')
        self.titleRect = self.titleText.get_rect(center=(650, 50))

        #Load available skins from DeckManager
        self.available_skins = Deck.DeckManager.get_available_skins()
        self.selected_skin_index = 0

        # Navigation buttons
        self.next_button = pygame.Rect(1100, 650, 150, 50)
        self.prev_button = pygame.Rect(50, 650, 150, 50)
        self.select_button = pygame.Rect(550, 650, 200, 50)
    
    def userInput(self, events):
        if events.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = events.pos
            if self.next_button.collidepoint(mouse_pos):
                self.selected_skin_index = (self.selected_skin_index + 1) % len(self.available_skins)
            elif self.prev_button.collidepoint(mouse_pos):
                self.selected_skin_index = (self.selected_skin_index - 1) % len(self.available_skins)
            elif self.select_button.collidepoint(mouse_pos):
                selected_skin = self.available_skins[self.selected_skin_index]
                Deck.DeckManager.set_current_skin(selected_skin)
                self.isFinished = True
                self.nextState = "StartState"
    
    def update(self):
        self.draw()
    
    def draw(self):
        screen = self.screen
        # Draw background
        screen.blit(self.background, (0, 0))

        # Draw title
        screen.blit(self.titleText, self.titleRect)

        # Draw current skin preview
        current_skin = self.available_skins[self.selected_skin_index]
        skin_image = Deck.DeckManager.load_skin_image(current_skin)
        skin_rect = skin_image.get_rect(center=(650, 350))
        screen.blit(skin_image, skin_rect)

        # Draw buttons
        pygame.draw.rect(screen, (0, 128, 0), self.next_button)  # Next button
        pygame.draw.rect(screen, (0, 128, 0), self.prev_button)  # Previous button
        pygame.draw.rect(screen, (0, 0, 128), self.select_button)  # Select button

        next_text = self.font.render("Next", True, 'white')
        prev_text = self.font.render("Previous", True, 'white')
        select_text = self.font.render("Select Skin", True, 'white')

        screen.blit(next_text, next_text.get_rect(center=self.next_button.center))
        screen.blit(prev_text, prev_text.get_rect(center=self.prev_button.center))
        screen.blit(select_text, select_text.get_rect(center=self.select_button.center))

        # Draw CRT overlay
        screen.blit(self.tvOverlay, (0, 0))
    
