import pygame, sys, glob, random

from pygame.mixer import stop # import pygame and sys
from Player import Player
from PlayerSystem import *
from Map import Map
from MapSystem import *
pygame.mixer.pre_init(44100, -16, 2, 512)#(frequency, size, channel, buffer)
# pygame.mixer.set_num_channels(64)#how many sound can play at once
clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('Pygame Window') # set the window name

WINDOW_SIZE = (1000, 600) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen
scale = 3
display = pygame.Surface((WINDOW_SIZE[0] / scale, WINDOW_SIZE[1] / scale))

player = Player()

player_image = pygame.image.load('Assets/Sprites/Adventurer-1.5/Individual Sprites/adventurer-idle-00.png')

scroll = [0, 0]
true_scroll = [0, 0]
is_jump = False
player_flip = False
# keep track current animation frame
animation_frame = 0
#animations dictonaries
player_animations = {}
#sfx dictionaries
sfx = {}
# backgrounds with paralax effect
backgrounds = [
    [0.10, #scroll speed
    [170, 10, 50, 900] #object rect
    ],
    [0.15, #scroll speed
    [400, 10, 70, 120] #object rect
    ],
    [0.15, #scroll speed
    [190, 10, 70, 500] #object rect
    ],
    [0.25, #scroll speed
    [410, 10, 70, 200] #object rect
    ],
    [0.25, #scroll speed
    [120, 10, 70, 400] #object rect
    ],
]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

# player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
# test_rect = pygame.Rect(100,100,100,50)
list_map_texture = [
    None,
    pygame.image.load('./Assets/Sprites/tiles/grass_tile.png').convert(),
    pygame.image.load('./Assets/Sprites/tiles/plain_dirt_tile.png').convert(),
    pygame.image.load('./Assets/Sprites/tiles/L_edge_grass_tile.png').convert(),
    pygame.image.load('./Assets/Sprites/tiles/R_edge_grass_tile.png').convert()
]
map_game = Map('Assets/Sprites/tiles/tile.txt', list_map_texture)
map_bp = map_game.load_map()

game_map = {}
CHUNK_SIZE = 8

#to render white line as collider outline
def render_collision(display, obj, scroll):
    WHITE = (255,255,255)

    pos = (obj.coll_rect.left - scroll[0], obj.coll_rect.top - scroll[1], (obj.coll_rect.right - obj.coll_rect.left), (obj.coll_rect.bottom - obj.coll_rect.top))

    pygame.draw.rect(display, WHITE, pos, 1)

# animation 
global animation_frames
# animation_frames = []
def load_animation(path, frame_duration):
    animation_name = path.split('/')[-1]#split path last dir name as animation's name
    animation_frame_data = [anim_frame for anim_frame in glob.iglob(path+"/*.png")]
    return sorted(animation_frame_data*frame_duration)

#assign sprite animation to player animation list
player_animations['idle'] = load_animation('./Assets/Sprites/Adventurer-1.5/idle', 7)
player_animations['run'] = load_animation('./Assets/Sprites/Adventurer-1.5/run', 7)
player_animations['jump'] = load_animation('./Assets/Sprites/Adventurer-1.5/jump', 12)
#this for change state between two animation
current_player_anim = player_animations['idle']

#sfx and music
#load sfx
sfx['jump'] = pygame.mixer.Sound('./Assets/Audio/footstep_concrete_000.ogg')
sfx['grass'] = [pygame.mixer.Sound('./Assets/Audio/footstep_grass_001.ogg'), pygame.mixer.Sound('./Assets/Audio/footstep_grass_002.ogg'), pygame.mixer.Sound('./Assets/Audio/footstep_grass_003.ogg')]
sfx_grass_timer = 0
for sfx_grass in sfx['grass']:
    sfx_grass.set_volume(0.3)
#load music
pygame.mixer.music.load('./Assets/Audio/Music/bgm.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
#GAME LOOP
while True: # game loop
    display.fill((133, 133, 133))
    # MOVE TO EVERY PIXEL ON SCREEN 
    # TO SIMULATE CAMERA MOVEMENT
    if sfx_grass_timer > 0:
        sfx_grass_timer -= 1

    heading_x = player.coll_rect.x - scroll[0] + 30
    heading_y = player.coll_rect.y - scroll[1]

    true_scroll[0] += (heading_x -  ((WINDOW_SIZE[0]/scale)/2) - (player.sprite.get_width() / 2))/32.05
    true_scroll[1] += (heading_y - scroll[1] - ((WINDOW_SIZE[1]/scale)/2) - (player.sprite.get_height() / 2))/32.05

    # copy, then convert to int
    scroll = true_scroll.copy()
    # scroll[0] = float(scroll[0])
    # scroll[1] = float(scroll[1])

    # Render Background 
    pygame.draw.rect(display, (120, 120, 120), pygame.Rect(0, 120, 340, 100))
    for background in backgrounds:
        background_rect = pygame.Rect(background[1][0] - scroll[0] * background[0], background[1][1] - scroll[1] * background[0], background[1][2], background[1][3])
        
        if background[0] == 0.10:
            pygame.draw.rect(display, (105, 105, 105), background_rect)
        if background[0] == 0.15:
            pygame.draw.rect(display, (87, 87, 87), background_rect)
        if  background[0] == 0.25:
            pygame.draw.rect(display, (66, 66, 66), background_rect)

    # Render Map 
    tile_rects = []
    # tile_rects = MapSystem.render(map_bp, map_game.list_texture, display, tile_rects, scroll)
    for y in range(2):
        for x in range(5):
            target_x = x -1 + int(scroll[0]/(CHUNK_SIZE*16))
            target_y = y + int(scroll[1]/(CHUNK_SIZE*16))
            target_chunk = str(target_x)+':'+str(target_y)
            if target_chunk not in game_map:
                # create chunk of map
                game_map[target_chunk] = map_game.generate_chunk(target_x, target_y, CHUNK_SIZE)
                #render only on chunk
            for tile in game_map[target_chunk]:
                display.blit(map_game.list_texture[tile[1]], (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16, tile[0][1]*16, 16, 16))

    ###########    Movement     #############
    player_movement = [0, 0]
    if moving_right:
        player_flip = False
        player_movement[0] += player.velocity
    if moving_left:
        player_flip = True
        player_movement[0] -= player.velocity
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2

    # this prevent player object move first before camera
    # start moving (caising jitter like)
    # scroll[0] += player_movement[0]
    
    # check player jump momentum
    if player_y_momentum > 3:
        player_y_momentum = 3
    
    player.coll_rect, collisions = move(player.coll_rect, player_movement, tile_rects)

    # AIR TIME WHEN PLAYER JUMP
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
        is_jump = False
        if player_movement[0] != 0 and sfx_grass_timer == 0:
            sfx_grass_timer = 20
            random.choice(sfx['grass']).play()
    else:
        air_timer += 1
    #animation handler change
    if is_jump:
        current_player_anim = player_animations['jump']
    elif moving_left or moving_right:
        current_player_anim = player_animations['run']
    else:
        current_player_anim = player_animations['idle']

    # RENDER PLAYER with current ANIMATION
        #reset animation frame to zero if reach the length
    if animation_frame >= len(current_player_anim):
        if is_jump:
            animation_frame = len(current_player_anim) - 1
        else:
            animation_frame = 0
        #freeze animation on last frame when in jump animation
    display.blit(pygame.transform.flip(pygame.image.load(current_player_anim[animation_frame]), player_flip, False), (player.coll_rect.x - scroll[0] -15, player.coll_rect.y - scroll[1] - 5))
    animation_frame += 1
    # SHOW PLAYER COLLISION
    # render_collision(display, player, scroll)
    # MOVEMENT HANDLER
    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_SPACE:
                if air_timer < 6:#it mean when player not in air
                    sfx['jump'].play()
                    player_y_momentum = -5
                    is_jump = True
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False

    # SCALE PIXEL SIZE 
    # THEN RENDER IT TO SCREEN
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps