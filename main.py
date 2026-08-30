
import pygame

from src.game import Game
from src.scenes import MainMenu

pygame.init()

game = Game()
game.load_scene(MainMenu)  # scene entry point
game.run()

pygame.quit()
