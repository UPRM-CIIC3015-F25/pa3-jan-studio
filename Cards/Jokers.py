import pygame
import random

class Jokers:
    def __init__(self,name: str, description: str, price = 5, chips = 0, mult = 0, image = None, isActive = False, variant = None):
        self.name = name
        self.description = description
        self.price = price
        self.chips = chips
        self.mult = mult
        self.image = image
        self.isActive = isActive
        self.variant = variant or VARIANT["BASE"]

    def __str__(self):
        return f"{self.name}: {self.description}"

    def sellPrice(self):
        return int(self.price * 0.6)
    # BONUS VARIANT
    def get_mult(self):
        if self.variant.name == "Holographic":
            return self.mult + self.variant.mult
        elif self.variant.name == "Polychrome:":
            return self.mult * self.variant.mult
        else:
            return self.mult

    def get_chips(self):
        if not self.variant:
            return self.chips
        return self.chips + self.variant.chips

class Variant:
    def __init__(self, name: str , mult: float, chips = 0, color = None):
        self.name = name
        self.mult = mult
        self.chips = chips
        self.color = color


VARIANT = { "BASE" : Variant("Base", mult = 0, chips = 0, color = None),
            "FOIL" : Variant("Foil", mult = 0, chips = 25, color = (169,215,255)),
            "HOLOGRAPHIC" : Variant("Holographic", mult = 5, chips = 0, color = (244,179,225)),
            "POLYCHROME" : Variant("Polychrome", mult= 1.25, chips = 0, color = (169,255,183))}
# for easier reference:
# color foil is blue
#color holographic is purple
#color polychrome is green
def select_variant():
    number = random.randint(1, 30)
    if number in [10, 11, 12, 13]:
        return VARIANT["FOIL"]
    elif number in [14, 15, 16, 17]:
        return VARIANT["HOLOGRAPHIC"]
    elif number in [20,21,24,27]:
        return VARIANT["POLYCHROME"]
    else:
        return VARIANT["BASE"]