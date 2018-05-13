import pygame, sys
import sceneExample, draw
import pymunk, pymunk.pygame_util

from time import time


# GLOBALS
phys_iterations = 5
fps_calculated  = 60
initalisation   = time()
running         = True
gravity         = [0, -1000]
delta           = 0
debug           = False
size            = [500, 500]
fps             = 60
n               = 0


# Setup physics
space            = pymunk.Space()
space.gravity    = gravity
space.iterations = phys_iterations
space.damping    = 0.90

scene = sceneExample.scene1(pygame, pymunk, space, size)


print("Physics setup ({})".format(time() - initalisation))

# Setup pygame
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
print("Pygame setup ({})".format(time() - initalisation))

if debug:
    print("DEBUG IS SET TO TRUE")
    draw_options = pymunk.pygame_util.DrawOptions(screen)


print("Starting main game loop ({})".format(time() - initalisation))
while running:
    scene.beforeLoop()
    screen.fill([0, 0, 0])

    data = scene.loop()
    if data[0] == 1: running = False




    if debug: space.debug_draw(draw_options)
    else: draw.simple(screen, data[1])


    if fps_calculated == 0: fps_calculated = 60
    space.step(1/fps_calculated)





    clock.tick(fps)
    fps_calculated = clock.get_fps()
    pygame.display.update()

    n += 1
    if n % fps == 0:
        print("There are {} objects spawned at fps {}".format(len(space.shapes), clock.get_fps()))
        n = 1

    scene.afterLoop()

pygame.quit()
print("Game stopped ({})".format(time() - initalisation))
