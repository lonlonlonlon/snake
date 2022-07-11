import pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))  # creates the screen
clock = pygame.time.Clock()

while True:
    clock.tick(1)
    keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    pygame.display.flip()
    print(keys)