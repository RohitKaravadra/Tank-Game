import pygame
import Variables
import Particles
import Sounds
import json

levels = dict()
file = open("Levels.txt")
data = file.read()
file.close()
levels = json.loads(data)

L = 0
level_no_preview = pygame.image.load("data//images//NoPreview.png")
level_preview = dict()
for index in range(len(levels)):
    try:
        level_preview.update(
            {"level{}".format(index + 1): pygame.transform.scale(
                pygame.image.load("data//images//level{}.png".format(index + 1)), (800, 400))})
    except FileNotFoundError:
        level_preview.update(
            {"level{}".format(index + 1): level_no_preview})


class bricks(pygame.sprite.Sprite):
    brick = {"concreat": [pygame.image.load("data//images//bricks.png").subsurface((0, 0, 60, 60)),
                          pygame.image.load("data//images//bricks.png").subsurface((60, 0, 60, 60)),
                          pygame.image.load("data//images//bricks.png").subsurface((120, 0, 60, 60))],
             "brick": [pygame.image.load("data//images//bricks.png").subsurface((0, 60, 60, 60)),
                       pygame.image.load("data//images//bricks.png").subsurface((60, 60, 60, 60))],
             "grass": [pygame.image.load("data//images//bricks.png").subsurface((0, 120, 60, 60))],
             "water": [pygame.image.load("data//images//bricks.png").subsurface((60, 120, 60, 60))]}

    def __init__(self, pos, strength, name):
        pygame.sprite.Sprite.__init__(self)
        self.strength = strength
        self.name = name
        self.image = bricks.brick[name][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Level:
    all_bricks = pygame.sprite.Group()

    def __init__(self, s_level):
        Level.all_bricks.empty()
        for tile in s_level:
            for data in s_level[tile]:
                brick = bricks(data[0], data[1], tile)
                Level.all_bricks.add(brick)

    def bullet_collision(self, sprite):

        hit = pygame.sprite.spritecollide(sprite, Level.all_bricks, False)
        if len(hit):
            if hit[0].name == "water":
                Sounds.sounds.water.play()
                color = pygame.Color("cyan")
                Particles.particle.add(sprite.rect.center, color)
                return 1
            else:
                if hit[0].name == "concreat":
                    color = pygame.Color("gray10")
                elif hit[0].name == "grass":
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("brown")
                if sprite.powerup:
                    Particles.particle.add(sprite.rect.center, color)
                    hit[0].kill()
                    Sounds.sounds.brick.play()
                    Particles.particle.add(sprite.rect.center, color)
                    return 0
            Particles.particle.add(sprite.rect.center, color)
            if hit[0].strength == 1:
                Sounds.sounds.brick.play()
                hit[0].kill()
            else:
                hit[0].strength -= 1
                hit[0].image = bricks.brick[hit[0].name][len(bricks.brick[hit[0].name]) - hit[0].strength]
            return 1
        else:
            return 0

    def player_collision(self, player):
        for i in Level.all_bricks:
            if i.rect.colliderect(player):
                return 1
        else:
            return 0


def initlevel():
    global L
    L = Level(levels["level{}".format(Variables.current_level)])
