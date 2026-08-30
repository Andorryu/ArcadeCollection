
from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from src.settings import Settings

if TYPE_CHECKING:
    from src.scenes import Scene


class Game:
    def __init__(self) -> None:
        self._running = True
        self._settings = Settings()
        self._current_scene: Scene | None = None
        self._clock = pygame.time.Clock()

        pygame.display.set_mode(
            size=self._settings.resolution,
            flags=self._settings.build_flags(),
            vsync=self._settings.vsync,
            display=self._settings.display,
        )

        pygame.display.set_caption("Arcade Collection")

    def load_scene(self, scene: type[Scene]):
        self._current_scene = scene(self)  # pass game into scene

    def run(self):
        if self._current_scene is None:
            raise ValueError("Attempted to run game without loading a scene!")

        fps = self._settings.framerate if self._settings.vsync else 0.0
        while self._running:
            dt = self._clock.tick(fps) / 1000.0
            self._current_scene.tick(dt)

    def quit(self):
        self._running = False
