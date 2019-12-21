import pygame
import random
import math


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class LightSource:
    def __init__(self, x, y):
        self.color = pygame.Color(255, 0, 0)
        self.x = x
        self.y = y
        self.radius = 5
        self.move_speed = 5

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self, keys):
        self.x, self.y = pygame.mouse.get_pos()

        # if self.x < 0: self.x = 0
        # if self.x > SCREEN_WIDTH - 1: self.x = SCREEN_WIDTH - 1
        # if self.y < 0: self.y = 0
        # if self.y > SCREEN_HEIGHT - 1: self.y = SCREEN_HEIGHT - 1


def draw_board(screen, elements):
    for start, end in elements:
        pygame.draw.line(screen, pygame.Color(255, 255, 255), start, end)


def generate_obstacles(num_of_obstacles):
    obstacles = []

    obstacles.append(((0, 0), (0, SCREEN_HEIGHT - 1)))
    obstacles.append(((SCREEN_WIDTH - 1, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1)))
    obstacles.append(((0, 0), (SCREEN_WIDTH - 1, 0)))
    obstacles.append(((0, SCREEN_HEIGHT - 1), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1)))

    for _ in range(num_of_obstacles):
        start = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
        end = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
        obstacles.append((start, end))

    return obstacles


def cast_rays(source, obstacles):
    num_of_rays = 100
    angle_increment = 2 * math.pi / num_of_rays
    max_ray_length = math.sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2)

    x3, y3 = source
    current_angle = 0
    rays = []

    def normalize(v_x, v_y):
        v_magnitude = math.sqrt(v_x ** 2 + v_y ** 2)
        v_x /= v_magnitude
        v_y /= v_magnitude
        return v_x, v_y

    def line_length(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    for _ in range(num_of_rays):
        dir_vector = math.cos(current_angle), math.sin(current_angle)
        candidates = []

        x4 = source[0] + dir_vector[0] * max_ray_length
        y4 = source[1] + dir_vector[1] * max_ray_length

        for p1, p2 in obstacles:
            x1, y1, x2, y2 = *p1, *p2

            if (denominator := (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)) == 0:
                continue
            else:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
                u = ((y1 - y2) * (x1 - x3) - (x1 - x2) * (y1 - y3)) / denominator

                if 0 < t < 1 and u > 0:
                    intersection_x = int(x1 + t * (x2 - x1))
                    intersection_y = int(y1 + t * (y2 - y1))
                    candidates.append((intersection_x, intersection_y))

        if candidates:
            rays.append((source, min(candidates, key=lambda x: line_length(*source, *x))))

        current_angle += angle_increment

    return rays


def draw_rays(screen, rays):
    for start, end in rays:
        pygame.draw.line(screen, pygame.Color(255, 255, 0), start, end)


def main():
    # background_color = pygame.Color(0, 0, 0)
    # borders_color = pygame.Color(255, 255, 255)
    # ray_color = pygame.Color(255, 255, 0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    light_source = LightSource(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    obstacles = generate_obstacles(5)

    while True:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pressed_keys = pygame.key.get_pressed()

        light_source.update(pressed_keys)
        rays = cast_rays((light_source.x, light_source.y), obstacles)

        screen.fill(pygame.Color(0, 0, 0))
        draw_rays(screen, rays)
        draw_board(screen, obstacles)
        light_source.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
