
from __future__ import annotations

import json
import os
import warnings
from dataclasses import dataclass
from enum import Enum

import pygame

SAVE_LOCATION = '/home/andorryu/projects/ArcadeCollection/saves/'
SAVE_FILENAME = 'settings.json'


class Resolution(Enum):
    HD = (1280, 720)
    FHD = (1920, 1080)
    QHD = (2560, 1440)
    UHD_4K = (3840, 2160)

    def format(self):
        return f'{self.value[0]}x{self.value[1]}'


@dataclass
class SettingsData:
    resolution: Resolution = Resolution.HD
    fullscreen: bool = True
    vsync: int = 0
    framerate: float = 60.0

    def as_dict(self) -> dict:
        return {
            'resolution': self.resolution.name,
            'fullscreen': self.fullscreen,
            'vsync': self.vsync,
            'framerate': self.framerate,
        }

    def parse(self, d: dict) -> SettingsData:
        return SettingsData(
            resolution=Resolution[d['resolution']],
            fullscreen=d['fullscreen'],
            vsync=d['vsync'],
            framerate=d['framerate'],
        )


@dataclass
class Settings:
    _save_data_location: str = f'{SAVE_LOCATION}{SAVE_FILENAME}' # change to Documents\ArcadeCollection\ for windows and
    _data: SettingsData = None

    def __post_init__(self):
        self._data = SettingsData()
        self.load() # load data from file
        if self._data.vsync and not self._data.fullscreen:
            warnings.warn('Warning: Vsync is on but fullscreen is not. Silently turning fullscreen on.')
            self._data.fullscreen = True

    def save(self):
        with open(self._save_data_location, 'w') as file:
            json.dump(self._data.as_dict(), file, indent=4)

    def load(self):
        try:
            with open(self._save_data_location, 'r') as file:
                self._data = SettingsData(self._data.parse(json.load(file)))
        except json.JSONDecodeError:
            print('Warning: Json failed to decode. Overwriting save with defaults.')
            self.save()
        except FileNotFoundError:
            print(f'Warning: {self._save_data_location} does not exist. Creating it now.')
            os.makedirs(SAVE_LOCATION, exist_ok=True)
            self.save()

    def build_flags(self):
        if self._data.vsync not in [-1, 0, 1]:
            raise ValueError("ERROR: vsync must be set to -1, 0, 1.")

        flags = 0
        if self._data.fullscreen:
            flags |= pygame.FULLSCREEN | pygame.SCALED
        if self._data.vsync:
            flags |= pygame.SCALED

        return flags

    # setter
    def set_data(
        self,
        resolution: Resolution | None = None,
        fullscreen: bool       | None = None,
        vsync:      int        | None = None,
        framerate:  float      | None = None,
    ):
        self._data.resolution = resolution if resolution is not None else self._data.resolution
        self._data.fullscreen = fullscreen if fullscreen is not None else self._data.fullscreen
        self._data.vsync      = vsync      if vsync      is not None else self._data.vsync
        self._data.framerate  = framerate  if framerate  is not None else self._data.framerate
        self.save()

    # getter
    def get_data(self) -> SettingsData:
        return self._data


# test saving and loading
if __name__ == "__main__":
    # Settings should be set to defaults and a new directory called "saves/" should be created if it doesn't exist.
    # Data should be stored in ./saves/settings.json
    import time
    settings = Settings()
    print('Saved initial settings!')
    time.sleep(5)
    # Change settings data. It should save it to the save file
    settings.set_data(
        resolution=Resolution.QHD,
        fullscreen=False,
        framerate=150.0,
    )
    print('Saved new settings!')
