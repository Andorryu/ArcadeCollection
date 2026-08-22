
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
            size=self._settings.get_data().resolution.value,
            flags=self._settings.build_flags(),
            vsync=self._settings._data.vsync,
        )

        pygame.display.set_caption("Arcade Collection")

    def load_scene(self, scene: Scene):
        self._current_scene = scene

    def run(self):
        if self._current_scene is None:
            raise ValueError("ERROR: Attempted to run game without loading a scene!")

        # call tick without framerate if vsync is active so that vsync doesn't fight pygame's framerate assertion
        fps = 0 if self._settings._data.vsync else self._settings._data.framerate

        while self._running:
            dt = self._clock.tick(fps) / 1000.0

            self._current_scene.tick(dt)

    def quit(self):
        self._running = False
