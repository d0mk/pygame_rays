import pygame


class LightSource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        self.color = pygame.Color(255, 0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()