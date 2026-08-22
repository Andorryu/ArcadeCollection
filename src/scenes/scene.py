
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.game import Game


class Scene(ABC):
    def __init__(self, game: Game) -> None:
        self._game = game

    def tick(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.quit()
            self._handle_event(event)

        self._handle_inputs()

        self._update(dt)

        self._draw()
        pygame.display.flip()

    @abstractmethod
    def _handle_event(self, event):
        ...

    @abstractmethod
    def _handle_inputs(self):
        ...

    @abstractmethod
    def _update(self, dt):
        ...

    @abstractmethod
    def _draw(self):
        ...
