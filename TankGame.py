import pygame
import Variables
import Functions
import Multiplayer
import Levels
import Sounds

pygame.display.set_caption("TANK WAR")

button1 = Functions.format_text("PLAY", ("xcenter", 360), Variables.CYAN)
button2 = Functions.format_text("LEVELS", ("xcenter", 420), Variables.CYAN)
button3 = Functions.format_text("EXIT", ("xcenter", 480), Variables.CYAN)
current_level = 1


def print_Buttons():
    button = 0
    if button1.collidepoint(Variables.Mouse_x, Variables.Mouse_y):
        Functions.format_text("PLAY", ("xcenter", 360), Variables.WHITE)
        button = 1
    else:
        Functions.format_text("PLAY", ("xcenter", 360), Variables.CYAN)

    if button2.collidepoint(Variables.Mouse_x, Variables.Mouse_y):
        Functions.format_text("LEVELS", ("xcenter", 420), Variables.WHITE)
        button = 2
    else:
        Functions.format_text("LEVELS", ("xcenter", 420), Variables.CYAN)

    if button3.collidepoint(Variables.Mouse_x, Variables.Mouse_y):
        Functions.format_text("EXIT", ("xcenter", 480), Variables.WHITE)
        button = 3
    else:
        Functions.format_text("EXIT", ("xcenter", 480), Variables.CYAN)
    return button


def Main_Menu():
    musicOn = False
    button = 0
    while True:
        if not musicOn:
            Sounds.sounds.music.play(-1)
            musicOn = True
        Variables.Mouse_x, Variables.Mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                Sounds.sounds.music.stop()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Sounds.sounds.click.play()
                    if button == 3:
                        Sounds.sounds.music.stop()
                        return
                    elif button == 1:
                        Sounds.sounds.music.stop()
                        musicOn = False
                        Levels.initlevel()
                        Variables.GAMEON = True
                        pygame.mouse.set_visible(False)
                        Multiplayer.play()
                        Variables.GAMEON = False
                        pygame.mouse.set_visible(True)
                    elif button == 2:
                        Variables.GAMEON = True
                        Variables.current_level = level_selector()
                        Variables.GAMEON = False

        Functions.Outline()
        button = print_Buttons()
        pygame.display.flip()


buttons = list()
current = ""


def print_levelbuttons():
    mx, my = pygame.mouse.get_pos()
    button = current
    for i in range(0, len(buttons)):
        color = Variables.CYAN
        if buttons[i].collidepoint(mx, my):
            color = Variables.WHITE
            button = i + 1
        if i + 1 == Variables.current_level:
            Functions.format_text("LEVEL{}{}".format(i + 1, '*'), (120, 160 + (40 * i)), color)
        else:
            Functions.format_text("LEVEL{}".format(i + 1), (120, 160 + (40 * i)), color)
    return button


def level_selector():
    total = len(Levels.levels)
    global current
    current = Variables.current_level
    global buttons
    for i in range(0, total):
        buttons.append(Functions.format_text("LEVEL", (120, 160 + (40 * i))))
    while True:
        Functions.Outline()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                buttons.clear()
                return Variables.current_level
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Sounds.sounds.click.play()
                    buttons.clear()
                    return current
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    buttons.clear()
                    return Variables.current_level
        current = print_levelbuttons()
        try:
            Variables.win.blit(Levels.level_preview["level{}".format(current)], (340, 160))
        except KeyError:
            Variables.win.blit(Levels.level_no_preview, (340, 160))
        pygame.display.flip()


Main_Menu()
pygame.quit()
