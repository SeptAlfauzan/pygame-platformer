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