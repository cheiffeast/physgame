import pygame, sys
import sceneExample
import pymunk, pymunk.pygame_util
import pygame.gfxdraw

from time import time
from math import degrees


# GLOBALS
phys_iterations = 5
fps_calculated  = 60
initalisation   = time()
running         = True
gravity         = [0, -1000]
delta           = 0
debug           = True
size            = [500, 500]
fps             = 60
n               = 0


# Setup physics
space            = pymunk.Space()
space.gravity    = gravity
space.iterations = 10
space.damping    = 0.90

#events = physics.scene(pygame, pymunk, space, size)
scene = sceneExample.scene1(pygame, pymunk, space, size)

img = pygame.image.load("default10x10.png")

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
    else:
        for line in data[1]:
            if line[0] == pymunk.Segment:
                pygame.draw.line(screen, [0, 255, 255], line[1], line[2], int(line[3]))

            if line[0] == pymunk.Circle:
                pygame.draw.circle(screen, [0, 255, 255], [int(line[1][0]), int(line[1][1])], int(line[2]))

            if line[0] == pymunk.Poly:
                pygame.draw.polygon(screen, [0, 255, 255], line[1])


    if fps_calculated == 0: fps_calculated = 60
    for i in range(phys_iterations): space.step(1/fps_calculated/phys_iterations)





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
