
# WIDTH, HEIGHT = 1280, 720
# screen = pygame.display.set_mode(
#     (WIDTH, HEIGHT),
#     flags=pygame.FULLSCREEN,
# )
# pygame.display.set_caption("Arcade Collection")
# clock = pygame.time.Clock()

# running = True
# while running:
#     dt = clock.tick(60) / 1000.0  # seconds; cap at 60 FPS

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 running = False

#     # update (nothing yet)

#     screen.fill((20, 20, 30))
    # pygame.display.flip()

import pygame

from globals import running
from scenes.scene import Scene


class Game:
    def __init__(self) -> None:
        self._current_scene: Scene = Scene.MainMenu()

    def run(self):
        while running:
            self._current_scene.tick()

