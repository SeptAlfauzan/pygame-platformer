import pygame


class Movement:
    @staticmethod
    def collide(rect, colliders):
        if type(colliders) is not list:
            colliders = [colliders]

        collisions = []
        for collider in colliders:
            if rect.colliderect(collider):
                collisions.append(collider)
        return collisions

    @staticmethod
    def _collision(rect, another_rect):
        collision_list = []
        if rect.colliderect(another_rect):
            collision_list.append(another_rect)
        return collision_list

    @staticmethod
    def move(obj_rect, move_axis, velocity, collisions):
        obj_rect.x += move_axis[0]

        collision_list = []
        for collision in collisions:
            if obj_rect.colliderect(collision):
                collision_list.append(collision)

        for col in collision_list:
            if move_axis[0] > 0:
                obj_rect.right = col.left
            elif move_axis[0] < 0:
                obj_rect.left = col.right

        obj_rect.y += move_axis[1]

        collision_list = []
        for collision in collisions:
            if obj_rect.colliderect(collision):
                collision_list.append(collision)

        for col in collision_list:
            if move_axis[1] > 0:
                obj_rect.bottom = col.top
            elif move_axis[1] < 0:
                print("col top")
                obj_rect.top = col.bottom
        return obj_rect

class Render:
    @staticmethod
    def render(obj, rect, screen, scroll=None):
        if scroll is None:
            scroll = [0, 0]
        screen.blit(obj.sprite, (rect.x - scroll[0], rect.y - scroll[1]))

    @staticmethod
    def render_collision(obj, screen, scroll=None):
        if scroll is None:
            scroll = [0, 0]
        color_white = (255, 255, 255)
        pos_n_size = (
            obj.position[0] - scroll[0], obj.position[1] - scroll[1], obj.sprite.get_width(), obj.sprite.get_height())
        pygame.draw.rect(screen, color_white, obj.coll_rect, 1)


##this only to test collision

class TestCol:
    is_collide = False
    rect = None

    def render(self, screen):
        self.rect = pygame.draw.rect(screen, (255, 255, 255), (64, 10, 10, 10))


