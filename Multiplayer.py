import pygame

from Player_properties import *
import time

Variables.win = pygame.display.set_mode((Variables.DISPLAY_WIDTH, Variables.DISPLAY_HEIGHT))

def Background():
    pygame.draw.rect(Variables.win, Variables.BLACK, (40, 80, 1200, 600))
    pygame.draw.rect(Variables.win, Variables.YELLOW, (40, 80, 1200, 600), 3)
    pygame.draw.rect(Variables.win, Variables.RED, (40, 40, 100, 10))
    pygame.draw.rect(Variables.win, Variables.RED, (1140, 40, 100, 10))
    pygame.draw.rect(Variables.win, Variables.WHITE, (40, 60, 100, 10))
    pygame.draw.rect(Variables.win, Variables.WHITE, (1140, 60, 100, 10))


def check_status():
    if Variables.player1.health <= 0:
        Particles.particle.total.clear()
        Particles.particle.add(Variables.player1.rect.center, Variables.GRAY, 40, 0.6)
        return 1, 2
    elif Variables.player2.health <= 0:
        Particles.particle.total.clear()
        Particles.particle.add(Variables.player2.rect.center, Variables.GRAY, 40, 0.6)
        return 1, 1
    else:
        return 0, 0


def print_result(all_sprites, winner):
    Sounds.sounds.explosion.play()
    while True:
        pygame.time.Clock().tick(30)
        Functions.Outline()
        Background()
        all_sprites.draw(Variables.win)
        Particles.particle.draw()
        pygame.display.flip()
        if not len(Particles.particle.total):
            Functions.Outline()
            Background()
            all_sprites.draw(Variables.win)
            Functions.format_text("PLAYER {} WON THE GAME".format(str(winner)), ("xcenter", 30), Variables.YELLOW)
            Functions.format_text("Press ESCAPE / Y - Button To Continue".format(str(winner)), ("xcenter", 60),
                                  Variables.YELLOW, 15)
            Particles.particle.draw()
            pygame.display.flip()
            while True:
                for i in pygame.event.get():
                    if i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_ESCAPE:
                            return
                    if i.type == pygame.JOYBUTTONDOWN:
                        if i.button == 3:
                            return


def play():
    all_sprites = pygame.sprite.Group()
    Variables.player1 = players(pygame.math.Vector2(40, 80), "keyboard", (0, 0, 60, 60), Variables.CYAN)

    # Check if a joystick is connected
    if pygame.joystick.get_count() == 0:
        Variables.player2 = players(pygame.math.Vector2(1180, 620), "keyboard2", (60, 0, 60, 60), Variables.PINK)
    else:
        Variables.player2 = players(pygame.math.Vector2(1180, 620), "controller", (60, 0, 60, 60), Variables.PINK)

    all_sprites.add(Levels.Level.all_bricks)
    all_sprites.add(Variables.player1, Variables.player2)

    last_time = time.time()
    while True:
        all_sprites.add(Variables.player1.total_bullets)
        all_sprites.add(Variables.player2.total_bullets)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # check inputs for player 1
                if event.key == pygame.K_b:
                    Variables.player1.add_bullet(True)
                elif event.key == pygame.K_v:
                    Variables.player1.add_bullet()

                # check inputs for player 2
                if pygame.joystick.get_count() == 0:
                    if event.key == pygame.K_RSHIFT:
                        Variables.player2.add_bullet(True)
                    elif event.key == pygame.K_RCTRL:
                        Variables.player2.add_bullet()

            # check joystick input for player 2
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    Variables.player2.add_bullet()
                elif event.button == 1:
                    Variables.player2.add_bullet(True)

        # update players
        Variables.player1.update()
        Variables.player2.update()

        # draw all sprites
        Functions.Outline()
        Background()
        all_sprites.draw(Variables.win)

        # check if the game is over
        result, winner = check_status()
        if result:
            print_result(all_sprites, winner)
            return

        # update particles
        Particles.particle.draw()
        pygame.display.flip()

        # update delta time
        Variables.deltaTime = (time.time() - last_time) * Variables.FPS
        last_time = time.time()
