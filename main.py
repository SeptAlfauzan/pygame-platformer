import sys
from Player import Player
from PlayerSystem import *
from Map import Map
from MapSystem import *
from pygame.locals import *

pygame.init()
WINDOW_SIZE = (1000, 600)
WINDOW_TITLE = 'entity component system test'
BG_COLOR = (32, 46, 64)
# scale size to 2x
scale = 3
DISPLAY = pygame.Surface((WINDOW_SIZE[0] / scale, WINDOW_SIZE[1] / scale))

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption(WINDOW_TITLE)

player = Player()
movement_sys = Movement()
list_collision = []

# collision test
test = TestCol()

#MAP
list_map_texture = [
    pygame.image.load('./Assets/Sprites/tiles/grass_tile.png').convert(),
    pygame.image.load('./Assets/Sprites/tiles/plain_dirt_tile.png').convert(),
    pygame.image.load('./Assets/Sprites/tiles/L_edge_grass_tile.png').convert(),
    pygame.image.load('./Assets/Sprites/tiles/R_edge_grass_tile.png').convert()
]
map_game = Map('Assets/Sprites/tiles/tile.txt', list_map_texture)
map_bp = map_game.load_map()

moveset = {
    'right': False,
    'left': False,
    'up': False,
    'down': False,
}


def close_game():
    pygame.quit()
    sys.exit()


def moving(obj):
    obj.movement = [0, 0]
    if moveset['right']:
        obj.movement = [1, 0]
        # movement_sys.move(obj, [1, 0])
    if moveset['left']:
        # movement_sys.move(obj, [-1, 0])
        obj.movement = [-1, 0]
    if moveset['up']:
        obj.movement = [0, -1]
        # movement_sys.move(obj, [0, -1])
    if moveset['down']:
        obj.movement = [0, 1]
    # movement_sys.move(obj, [0, 1])



while True:
    DISPLAY.fill(BG_COLOR)
    tile_rects = []

    Render.render_collision(player, DISPLAY)
    # render map
    tile_rects = MapSystem.render(map_bp, map_game.list_texture, DISPLAY, tile_rects, [0, 0])

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_d:
                moveset['right'] = True
                # point_location[0] += 1
            if event.key == K_a:
                moveset['left'] = True
                # point_location[0] += -1
            if event.key == K_w:
                moveset['up'] = True
                # point_location[1] += -1
            if event.key == K_s:
                moveset['down'] = True
                # point_location[1] += 1

        if event.type == KEYUP:
            if event.key == K_d:
                moveset['right'] = False
            if event.key == K_a:
                moveset['left'] = False
            if event.key == K_w:
                moveset['up'] = False
            if event.key == K_s:
                moveset['down'] = False

        if event.type == QUIT:
            # print(player.sprite)
            close_game()

    # test.render(DISPLAY)

    # DISPLAY.blit(map_game.list_texture[0], (0, 0))
    player_rect = movement_sys.move(player.coll_rect, player.movement, player.velocity, tile_rects)
    moving(player)
    Render.render(player, player_rect, DISPLAY)

    screen.blit(pygame.transform.scale(DISPLAY, WINDOW_SIZE), (0, 0))
    pygame.display.update()
