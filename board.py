import pygame
import random
from light_source import LightSource
from rays import cast_rays


class Board:
    def __init__(self):
        pygame.init()
        self.initialize_board()
        self.generate_obstacles()

    
    def initialize_board(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.FPS = 120
        self.clock = pygame.time.Clock()
        self.num_of_obstacles = 5
        self.rays = None
        self.ray_color = pygame.Color(255, 255, 0)
        self.wall_color = pygame.Color(255, 255, 255)
        self.background_color = pygame.Color(0, 0, 0)

    
    def generate_obstacles(self):
        self.obstacles = []

        self.obstacles.append(((0, 0), (0, self.screen_height - 1)))
        self.obstacles.append(((self.screen_width - 1, 0), (self.screen_width - 1, self.screen_height - 1)))
        self.obstacles.append(((0, 0), (self.screen_width - 1, 0)))
        self.obstacles.append(((0, self.screen_height - 1), (self.screen_width - 1, self.screen_height - 1)))

        for _ in range(self.num_of_obstacles):
            start = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            end = random.randint(0, self.screen_width), random.randint(0, self.screen_height)
            self.obstacles.append((start, end))

    
    def draw(self):
        for start, end in self.rays:
            pygame.draw.line(self.screen, self.ray_color, start, end)

        for start, end in self.obstacles:
            pygame.draw.line(self.screen, self.wall_color, start, end, 2)


    def start(self):
        light_source = LightSource(self.screen_width // 2, self.screen_height // 2)

        while True:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # pressed_keys = pygame.key.get_pressed()

            light_source.update()
            self.rays = cast_rays((light_source.x, light_source.y), self.obstacles, self.screen_width, self.screen_height)

            self.screen.fill(self.background_color)
            self.draw()
            light_source.draw(self.screen)

            pygame.display.flip()