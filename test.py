import pygame

from scripts import generate_level
from engine import world


window = pygame.display.set_mode((500, 500), 0, 32)
clock = pygame.time.Clock()

w = world.World(None)


tiles = []
aa = [1, 2, 3, 4, 5,6, 7, 8, 9]
# create the possible tiles
tiles.append(generate_level.Tile2D(1, aa, [4,7,1], aa, [1,4,7,9]))
tiles.append(generate_level.Tile2D(2, aa, [3,5,9], aa, [8,6]))
tiles.append(generate_level.Tile2D(3, aa, [2], aa, [6,8,2]))
tiles.append(generate_level.Tile2D(4, aa, [1,4,7,8,6], aa, [1,4,7,9]))
tiles.append(generate_level.Tile2D(5, aa, [2], aa, [8,6,2]))
tiles.append(generate_level.Tile2D(6, aa, [3,5,9], aa, [9,1,4,7]))
tiles.append(generate_level.Tile2D(7, aa, [1,4,7,8,6], aa, [1,4,7,9]))
tiles.append(generate_level.Tile2D(8, aa, [5,3,9], aa, [1,4,7,9]))
tiles.append(generate_level.Tile2D(9, aa, [6,1,4,7], aa, [6,2,8]))

wcf = generate_level.LevelGenerator2D(w, tiles, 5, 5)
# wcf.collapse()

# for y in range(5):
#    print(list(wcf.grid[y][x].state for x in range(5)))
images = []
img = pygame.image.load("assets/tileset.png").convert_alpha()
width = 8
height = 8
images.append(pygame.transform.scale(pygame.image.load("assets/empty.png"), (100, 100)).convert_alpha())
for y in range(3): 
    for x in range(3): images.append(pygame.transform.scale(img.subsurface((x*width, y*height, width, height)), (100, 100)))

running = True
while running:
    window.fill((0, 0, 0))
    # render the objects
    for x in range(5):
        for y in range(5):
            window.blit(images[wcf.grid[y][x].get_state()], (x*100, y*100))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                wcf.iter_collapse()

    pygame.display.update()
    clock.tick(30)

pygame.quit()

