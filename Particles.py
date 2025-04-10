
import pygame
import random
import Variables

pygame.init()


class particle:
    total = []

    def __init__(self, pos, color, speed):
        self.pos = pos
        self.particles = dict()
        self.dimen = (0, 0)
        self.color = color
        self.speed = speed

    def update(self):
        delete = []
        for i in self.particles.keys():
            if self.particles[i][2] >= 8:
                delete.append(i)
            else:
                self.particles[i][0] += random.randrange(-2, 3)
                self.particles[i][1] += random.randrange(-2, 3)
                self.particles[i][2] += self.speed * Variables.deltaTime
                self.particles[i][3] += self.speed * Variables.deltaTime
            pygame.draw.rect(Variables.win, self.color, (int(self.particles[i][0] - self.particles[i][2]/2),
                                               int(self.particles[i][1] - self.particles[i][3]/2),
                                               3, 3))
        for i in delete:
            self.particles.pop(i)

        if not len(self.particles):
            return 1

    @classmethod
    def add(cls, pos, color=Variables.RED, no=30, speed=1):
        part = particle(pos, color, speed)
        particle.total.append(part)
        for i in range(0, no):
            part.particles.update({i: [pos[0], pos[1], part.dimen[0], part.dimen[1]]})

    @classmethod
    def draw(cls):
        for i in particle.total:
            if i.update():
                particle.total.remove(i)
        else:
            return













