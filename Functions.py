import pygame
import Variables

pygame.init()

joy = 0

if not pygame.joystick.get_count() == 0:
    joy = pygame.joystick.Joystick(0)
    joy.init()

# ---------------------------------------------------------------------
# Function To Print Text(Returns A Rect value)
# ---------------------------------------------------------------------


def format_text(text, pos, color=Variables.WHITE, size=25, text_type="Times New Roman"):
    text_formate = pygame.font.SysFont(text_type, size)
    text_rect = text_formate.render(text, True, color)
    rect = list(pygame.Surface.get_rect(text_rect))
    if pos == "center":
        pos = ((Variables.DISPLAY_WIDTH - rect[2])/2, (Variables.DISPLAY_HEIGHT - rect[3])/2)
    elif pos == "centertop":
        pos = ((Variables.DISPLAY_WIDTH - rect[2])/2, 2)
    elif pos == "topleft":
        pos = (2, 2)
    elif pos == "topright":
        pos = (Variables.DISPLAY_WIDTH - rect[2] - 2, 2)
    elif pos == "centerright":
        pos = (Variables.DISPLAY_WIDTH - rect[2] - 2, (Variables.DISPLAY_HEIGHT - rect[3])/2)
    elif pos == "centerleft":
        pos = (2, (Variables.DISPLAY_HEIGHT - rect[3])/2)
    elif pos[0] == "xcenter":
        pos = ((Variables.DISPLAY_WIDTH - rect[2])/2, pos[1])
    elif pos[1] == "ycenter":
        pos = (pos[0], (Variables.DISPLAY_HEIGHT - rect[3])/2)
    Variables.win.blit(text_rect, pos)
    rect = pygame.Rect(pos[0], pos[1], rect[2], rect[3])
    return rect

# ------------------------------------------------------------------------------------
# Function To Outline The game
# ------------------------------------------------------------------------------------


def Outline():
    pygame.draw.rect(Variables.win, pygame.Color("yellow"), (0, 0, Variables.DISPLAY_WIDTH, Variables.DISPLAY_HEIGHT))
    pygame.draw.rect(Variables.win, pygame.Color("gray15"), (20, 20, Variables.DISPLAY_WIDTH - 40, Variables.DISPLAY_HEIGHT - 40))
    format_text("TANKS", "centertop", Variables.BLACK, 20)
    if not Variables.GAMEON:
        format_text("TANKS", ("xcenter", 120), pygame.Color("green"), 100, "Algerian")
        format_text("TANKS", ("xcenter", 122), pygame.Color("yellow"), 100, "Algerian")
        format_text("multiplayer", ("xcenter", 220), pygame.Color("cyan"), 30)
        format_text("multiplayer", ("xcenter", 222), pygame.Color("darkcyan"), 30)
