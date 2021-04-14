import pygame


class MapSystem:
    @staticmethod
    def render(list_map, list_texture, display, tile_rects, scroll):
        tile_size = [list_texture[0].get_width(), list_texture[0].get_height()]
        x = 0
        y = 5

        ###############
        # BUG
        ###############
        for row in list_map:
            x = 0
            for col in row:
                # print(col)
                if col == ".":
                    display.blit(list_texture[1], (x * tile_size[0] - scroll[0], y * tile_size[1] - scroll[1]))
                    tile_rects.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))
                    #tile rects
                if col == "^":
                    display.blit(list_texture[0], (x * tile_size[0] - scroll[0], y * tile_size[1] - scroll[1]))
                    tile_rects.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))
                    #tile rects
                if col == "<":
                    display.blit(list_texture[2], (x * tile_size[0] - scroll[0], y * tile_size[1] - scroll[1]))
                    tile_rects.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))
                    #tile rects
                if col == ">":
                    display.blit(list_texture[3], (x * tile_size[0] - scroll[0], y * tile_size[1] - scroll[1]))
                    tile_rects.append(pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))
                    # tile rects
                x += 1
            y += 1
        return tile_rects