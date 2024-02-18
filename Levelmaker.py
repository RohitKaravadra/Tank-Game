import pygame
import json

pygame.init()

win = pygame.display.set_mode((1280, 720))


def Background():
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (0, 0, 0), (40, 80, 1200, 600))
    pygame.draw.rect(win, (225, 225, 0), (40, 80, 1200, 600), 3)


def format_text(text, size=25):
    text_format = pygame.font.SysFont("Times New Roman", size)
    return text_format.render(text, True, (225, 225, 225))


bricksImages = {"concreat": pygame.image.load("data\\images\\bricks.png").subsurface((0, 0, 60, 60)),
                "brick": pygame.image.load("data\\images\\bricks.png").subsurface((0, 60, 60, 60)),
                "grass": pygame.image.load("data\\images\\bricks.png").subsurface((0, 120, 60, 60)),
                "water": pygame.image.load("data\\images\\bricks.png").subsurface((60, 120, 60, 60))}

level = {'concreat': [], 'brick': [], 'grass': [], 'water': []}
currentTile = 0
tileNames = list(bricksImages.keys())
currentTileName = format_text(tileNames[currentTile])
tileHealths = (3, 2, 1, 0)
currentPos = (0, 0)


def is_empty_level():
    for brick in level:
        if len(level[brick]) > 0:
            return False
    return True


def save_level():
    if is_empty_level():
        return

    current_levels = dict()
    file = open("Levels.txt", 'r')
    data = file.read()
    file.close()
    if len(data) > 1:
        current_levels = json.loads(data)
        if len(current_levels) > 9:
            print("Cant Add Levels... \nDelete Level to Add new")
            return

    current_levels.update({"level{}".format(len(current_levels) + 1): level})
    data = json.dumps(current_levels)
    file = open("Levels.txt", 'w')
    file.write(data)
    file.close()
    print("Level {} Added".format(len(current_levels)))


def add_tile():
    if not currentPos == (0, 0):
        remove_tile()
        level[tileNames[currentTile]].append([currentPos, tileHealths[currentTile]])


def remove_tile():
    if not currentPos == (0, 0):
        for brick in level.keys():
            for data in level[brick]:
                if data[0] == currentPos:
                    level[brick].remove(data)
                    return


def set_current_pos():
    global currentPos
    for x in range(40, 1211, 60):
        for y in range(80, 651, 60):
            if pygame.Rect(x, y, 60, 60).collidepoint(mx, my):
                currentPos = (x, y)
                return
    currentPos = (0, 0)


def display_tiles():
    for brick in level.keys():
        for data in level[brick]:
            win.blit(bricksImages[brick], data[0])


def delete_last():
    file = open("Levels.txt", 'r')
    data = file.read()
    file.close()
    if len(data) > 0:
        current_levels = json.loads(data)
        if len(current_levels) > 3:
            current_levels.pop("level{}".format(len(current_levels)))
            data = json.dumps(current_levels)
            file = open("Levels.txt", 'w')
            file.write(data)
            file.close()
            print("Level {} Deleted".format(len(current_levels) + 1))
        else:
            print("No Custom Levels To Delete")


def mainloop():
    while True:
        global mx, my, currentTileName, currentTile
        mx, my = pygame.mouse.get_pos()
        set_current_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                    return
                elif event.key == pygame.K_RETURN:
                    save_level()
                elif event.key == pygame.K_SPACE:
                    if currentTile == 3:
                        currentTile = 0
                    else:
                        currentTile += 1
                    currentTileName = format_text(tileNames[currentTile])
                elif event.key == pygame.K_DELETE:
                    delete_last()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    add_tile()
                elif event.button == 3:
                    remove_tile()

        Background()
        win.blit(currentTileName, (80, 40))
        display_tiles()
        pygame.display.flip()


mainloop()
