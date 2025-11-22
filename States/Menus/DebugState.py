import pygame
from States.Core.StateClass import State


#---------- Debug Overlay State ----------
class DebugState(State):
    def __init__(self, nextState: str = "", game_state=None):
        super().__init__(nextState)
        self.game_state = game_state
        self.visible = False  # Whether the debug UI is shown

        # === Fonts and overlay setup ===
        self.font = pygame.font.Font("graphics/Text/m6x11.ttf", 24)
        self.smallFont = pygame.font.Font("graphics/Text/m6x11.ttf", 18)

        self.bg_surface = pygame.Surface((400, 250), pygame.SRCALPHA)
        self.bg_surface.fill((10, 10, 10, 200))  # semi-transparent dark background

        # === Menu Text ===
        self.lines = [
            "=== DEBUG MENU ===",
            "↓ Open/Close Menu with DOWN arrow",
            "→ Skip current blind with RIGHT arrow",
            "↑ Add more money with UP arrow",
            "← Add a Joker with LEFT arrow + # (0–9)",
            "",
            "Player money:",
            "Current level:",
            "Time since start:",
        ]

    # ==============================
    # Update & Draw
    # ==============================
    def update(self):
        if self.visible:
            self.draw()

    def draw(self):
        if self.visible:
            self._draw_overlay()

    def _draw_overlay(self):
        screen = self.screen
        screen_width = self.screen.get_width()
        if self.game_state and hasattr(self.game_state, 'draw'):
            self.game_state.draw()

        # --- Position overlay at top-right ---
        overlay_x = screen_width - self.bg_surface.get_width() - 50
        overlay_y = 50
        screen.blit(self.bg_surface, (overlay_x, overlay_y))

        # --- Draw Text lines ---
        y = overlay_y + 20
        for line in self.lines[:6]:  # draw menu header & controls
            color = (255, 255, 100) if "===" in line else (255, 255, 255)
            txt = self.smallFont.render(line, True, color)
            screen.blit(txt, (overlay_x + 20, y))
            y += 25

        # --- Dynamic info alignment ---
        label_x = overlay_x + 20
        value_x = overlay_x + 260

        # === Player Money ===
        money = 0
        if self.game_state and hasattr(self.game_state, "playerInfo"):
            money = getattr(self.game_state.playerInfo, "playerMoney", 0)
        txt_money_label = self.smallFont.render("Player money:", True, (255, 255, 255))
        txt_money_value = self.smallFont.render(f"{money}$", True, (0, 255, 0))
        screen.blit(txt_money_label, (label_x, y))
        screen.blit(txt_money_value, (value_x, y))
        y += 25

        # === Current Level (from LevelManager) ===
        current_level = "N/A"
        if self.game_state and hasattr(self.game_state, "playerInfo"):
            player = self.game_state.playerInfo
            lm = player.levelManager
            if lm is not None:
                subLevel = lm.curSubLevel
                if subLevel is not None:
                    # use bossLevel if present, otherwise blind name; guard with getattr
                    boss = subLevel.bossLevel
                    if boss:
                        current_level = boss
                    else:
                        current_level = subLevel.blind.name
                        if current_level is not None:
                            current_level = current_level.capitalize()
        txt_level_label = self.smallFont.render("Current level:", True, (255, 255, 255))
        txt_level_value = self.smallFont.render(str(current_level), True, (180, 180, 255))
        screen.blit(txt_level_label, (label_x, y))
        screen.blit(txt_level_value, (value_x, y))
        y += 25

        # === Time since start ===
        seconds = int(pygame.time.get_ticks() / 1000)
        txt_time_label = self.smallFont.render("Time since start:", True, (255, 255, 255))
        txt_time_value = self.smallFont.render(f"{seconds}s", True, (180, 180, 255))
        screen.blit(txt_time_label, (label_x, y))
        screen.blit(txt_time_value, (value_x, y))

    # ==============================
    # Input Handling
    # ==============================
    def userInput(self, events):
        if events.type == pygame.KEYDOWN:
            # ↓ Toggle visibility
            if events.key == pygame.K_DOWN:
                self.visible = not self.visible
                print(f"[DEBUG] UI {'shown' if self.visible else 'hidden'}")

            # → Skip current blind

            #------- DO NOT TOUCH THIS ELIF ---------
            elif self.visible and events.key == pygame.K_RIGHT:
                print("[DEBUG] Skipping current blind...")
                if State.screen:
                    State.screenshot = State.screen.copy()

                if self.game_state:
                    player = self.game_state.playerInfo
                    levelManager = player.levelManager
                    if levelManager.curSubLevel is not None:
                        player.roundScore = levelManager.curSubLevel.score
                        levelManager.update()
                    else:
                        player.levelFinished = True

                    # If LevelManager set playerWins (no more levels), go to GameWinState
                    if player.levelManager.playerWins:
                        self.game_state.nextState = "GameWinState"
                        self.game_state.isFinished = True
                    else:
                        # Otherwise go to level selection as usual
                        self.game_state.nextState = "LevelSelectState"
                        self.game_state.isFinished = True
            elif self.visible and events.key == pygame.K_UP:
                print("[DEBUG] Adding 1$ to player money...")
                if self.game_state:
                    player = self.game_state.playerInfo
                    player.playerMoney += 10
