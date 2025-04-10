import pygame
import Variables
import Levels
import Particles
import Functions
import Sounds


class players(pygame.sprite.Sprite):

    def __init__(self, pos, type, subsurface, color=Variables.WHITE):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 1
        self.bulletSpeed = 3
        self.pos = pos
        self.health = 100
        self.power = 100
        self.color = color
        self.up = pygame.transform.rotate(pygame.image.load("data\\images\\players.png").subsurface(subsurface), 0)
        self.down = pygame.transform.rotate(pygame.image.load("data\\images\\players.png").subsurface(subsurface), 180)
        self.right = pygame.transform.rotate(pygame.image.load("data\\images\\players.png").subsurface(subsurface), -90)
        self.left = pygame.transform.rotate(pygame.image.load("data\\images\\players.png").subsurface(subsurface), 90)
        self.image = self.up
        self.type = type
        self.total_bullets = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos.x, pos.y)
        self.front = pygame.Rect(0, 0, 1, 1)

    class bullets(pygame.sprite.Sprite):

        def __init__(self, player, pos, speed, powerup):
            pygame.sprite.Sprite.__init__(self)
            self.bullet_speed = speed
            self.powerup = powerup
            if speed.x == 0:
                if self.powerup:
                    self.image = pygame.Surface((5, 15))
                else:
                    self.image = pygame.Surface((3, 10))
            else:
                if self.powerup:
                    self.image = pygame.Surface((15, 5))
                else:
                    self.image = pygame.Surface((10, 3))
            self.image.fill(player.color)
            self.rect = self.image.get_rect()
            self.pos = pos
            self.rect.center = pos
            self.total = pygame.sprite.Group()
            player.total_bullets.add(self)

        def update(self, player):
            if 40 < self.rect.center[0] < 1240 and 80 < self.rect.center[1] < 680 and not self.collision(player) \
                    and not Levels.L.bullet_collision(self):
                if not self.bullets_collision(player):
                    if self.powerup:
                        Particles.particle.add(self.rect.center, Variables.YELLOW, 5)
                    self.pos += self.bullet_speed * Variables.deltaTime
                    self.rect.center = self.pos
            else:
                self.kill()

        def collision(self, player):
            if player.rect.colliderect(self.rect):
                if self.powerup:
                    Sounds.sounds.rockethit.play()
                else:
                    Sounds.sounds.playerhit.play()
                if player == Variables.player1:
                    Particles.particle.add(self.rect.center, Variables.player2.color)
                else:
                    Particles.particle.add(self.rect.center, Variables.player1.color)
                player.update_health(self.rect.center, self)
                return 1
            else:
                return 0

        def bullets_collision(self, player):
            hit = pygame.sprite.spritecollide(self, player.total_bullets, False)
            if len(hit):
                if hit[0].powerup and not self.powerup:
                    Particles.particle.add(self.rect.center, player.color)
                    self.kill()
                    return 1
                elif self.powerup and not hit[0].powerup:
                    Particles.particle.add(self.rect.center, player.color)
                    hit[0].kill()
                    return 0
                else:
                    Particles.particle.add(self.rect.center, player.color)
                    hit[0].kill()
                    self.kill()
                    return 1
            else:
                return 0

    def update(self):
        self.update_movement()
        self.update_bullet()
        if Variables.player1.health > 0:
            pygame.draw.rect(Variables.win, Variables.GREEN, (40, 40, Variables.player1.health, 10))
        if Variables.player2.health > 0:
            pygame.draw.rect(Variables.win, Variables.GREEN, (1140, 40, Variables.player2.health, 10))
        if Variables.player1.power > 0:
            pygame.draw.rect(Variables.win, Variables.CYAN, (40, 60, Variables.player1.power, 10))
        if Variables.player2.power > 0:
            pygame.draw.rect(Variables.win, Variables.CYAN, (1140, 60, Variables.player2.power, 10))
        if self.power < 100:
            self.power += 0.1 * Variables.deltaTime
            if self.power >= 100:
                Sounds.sounds.powerup.play()

    def update_movement(self):

        if self.type == "keyboard":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.image = self.up
            elif keys[pygame.K_s]:
                self.image = self.down
            elif keys[pygame.K_d]:
                self.image = self.right
            elif keys[pygame.K_a]:
                self.image = self.left
            else:
                return
        elif self.type == "keyboard2":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.image = self.up
            elif keys[pygame.K_DOWN]:
                self.image = self.down
            elif keys[pygame.K_RIGHT]:
                self.image = self.right
            elif keys[pygame.K_LEFT]:
                self.image = self.left
            else:
                return
        elif self.type == "controller":
            if not pygame.joystick.get_count() == 0:
                axis1 = round(Functions.joy.get_axis(0), 0)
                axis2 = round(Functions.joy.get_axis(1), 0)
                if axis1 == 0 and axis2 < 0:
                    self.image = self.up
                elif axis1 == 0 and axis2 > 0:
                    self.image = self.down
                elif axis1 < 0 and axis2 == 0:
                    self.image = self.left
                elif axis1 > 0 and axis2 == 0:
                    self.image = self.right
                else:
                    return
        else:
            return

        size = self.rect.size
        if self.image == self.up:
            self.front = pygame.Rect(self.rect.topleft[0] + 2, self.rect.midtop[1] - 2, size[0] - 4, 1)
        elif self.image == self.down:
            self.front = pygame.Rect(self.rect.bottomleft[0] + 2, self.rect.midbottom[1] + 2, size[0] - 4, 1)
        elif self.image == self.left:
            self.front = pygame.Rect(self.rect.midleft[0] - 2, self.rect.topleft[1] + 2, 1, size[1] - 4)
        elif self.image == self.right:
            self.front = pygame.Rect(self.rect.midright[0] + 2, self.rect.topright[1] + 2, 1, size[1] - 4)

        if not (self.player_collision() or Levels.L.player_collision(self.front)):
            dir = pygame.Vector2(0, 0)
            if self.image == self.up:
                if self.pos.y > 80:
                    dir.y = -1
            elif self.image == self.down:
                if self.pos.y < 620:
                    dir.y = 1
            elif self.image == self.left:
                if self.pos.x > 40:
                    dir.x = -1
            elif self.image == self.right:
                if self.pos.x < 1180:
                    dir.x = 1

            self.pos += dir * self.speed * Variables.deltaTime
            self.rect.topleft = self.pos

    def add_bullet(self, powerup=False):
        if powerup:
            if self.power >= 50:
                self.power -= 50
            else:
                return
        if powerup:
            Sounds.sounds.rocket.play()
        else:
            Sounds.sounds.bullet.play()
        if self.image == self.up:
            players.bullets(self, self.rect.midtop, pygame.math.Vector2(0, -1) * self.bulletSpeed, powerup)
        elif self.image == self.down:
            players.bullets(self, self.rect.midbottom, pygame.math.Vector2(0, 1) * self.bulletSpeed, powerup)
        elif self.image == self.right:
            players.bullets(self, self.rect.midright, pygame.math.Vector2(1, 0) * self.bulletSpeed, powerup)
        elif self.image == self.left:
            players.bullets(self, self.rect.midleft, pygame.math.Vector2(-1, 0) * self.bulletSpeed, powerup)

    def update_bullet(self):
        player = Variables.player1
        if self == Variables.player1:
            player = Variables.player2
        self.total_bullets.update(player)

    def player_collision(self):
        player = Variables.player1
        if self == Variables.player1:
            player = Variables.player2

        return player.rect.colliderect(self.front)

    def update_health(self, bullet_pos, bullet):
        if self.health > 0:
            if bullet.powerup:
                if self.health > 20:
                    self.health -= 20
                else:
                    self.health = 0
            elif self.rect.centerx - 10 < bullet_pos[0] < self.rect.centerx + 10 or \
                    self.rect.centery - 10 < bullet_pos[1] < self.rect.centery + 10 and self.health > 5:
                self.health -= 10
            else:
                self.health -= 5
