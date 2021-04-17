class Map:

    def __init__(self, map_path, list_texture):
        self.map_path = map_path
        self.list_texture = list_texture

    def load_map(self):
        f = open(self.map_path, 'r')
        data_map = f.read()
        f.close()

        # split each row
        data_map = data_map.split('\n')
        game_map = []
        x =0
        for row in data_map:
            x += 1
            game_map.append(list(row))

        return game_map

    def generate_chunk(self, x, y, CHUNK_SIZE):

        chunk_data = []
        for y_pos in range(CHUNK_SIZE):
            for x_pos in range(CHUNK_SIZE):
                target_x = x * CHUNK_SIZE + x_pos
                target_y = y * CHUNK_SIZE + y_pos
                tile_type = 0
                if target_y > 5:
                    tile_type  = 2
                if target_y == 5:
                    tile_type  = 1
                #for grass tile
                #for plant tile
                if tile_type != 0:
                    chunk_data.append([[target_x,target_y], tile_type])

        return chunk_data

# map = Map('Assets/Sprites/tiles/tile.txt')
# arr_map = map.load_map()
#
# air = 0
# for row in arr_map:
#     for col in row:
#         if col == " ":
#             air += 1
#         print(col, end='')
# print(air)