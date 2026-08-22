
from abc import ABC, abstractmethod


class Scene(ABC):

    def tick(self):
        self._handle_events()
        self._handle_inputs()
        self._update()
        self._draw()

    @abstractmethod
    def _handle_events(self):
        ...

    @abstractmethod
    def _handle_inputs(self):
        ...

    @abstractmethod
    def _update(self):
        ...

    @abstractmethod
    def _draw(self):
        ...