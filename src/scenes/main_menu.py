
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from src.scenes.scene import Scene


class MainMenu(Scene):
    def _handle_event(self, event: Event):
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            # for debug, quit game on esc key
            if key[pygame.K_ESCAPE]:
                self._game.quit()
    
    def _handle_inputs(self):
        ...

    def _update(self, dt):
        ...

    def _draw(self):
        ...
