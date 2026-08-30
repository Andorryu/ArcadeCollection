
from __future__ import annotations

import json
import os
import warnings
from dataclasses import dataclass

import pygame

SAVE_LOCATION = '/home/andorryu/projects/ArcadeCollection/saves/settings.json' # change to Documents\ArcadeCollection\ for windows and

RESOLUTIONS = {
    '1280x720': (1280, 720),
    '1920x1080': (1920, 1080),
    '2560x1440': (2560, 1440),
    '3840x2160': (3840, 2160),
}


@dataclass
class Settings:
    display: int = 0 # Which display the game shows on. e.g., 0, 1, 2, ...
    adaptive_resolution: bool = True # make resolution display's resolution
    resolution: tuple[int, int] = None
    vsync: int = 0
    fullscreen: bool = True
    framerate: float = 60.0

    def __post_init__(self):
        self.load_and_sync()

    def _as_dict(self) -> dict:
        """
            Sets settings data in dictionary format, to be saved in json format.
        """
        return {
            'display': self.display,
            'resolution': 'adaptive' if self.adaptive_resolution else self.resolution,
            'vsync': self.vsync,
            'fullscreen': self.fullscreen,
            'framerate': self.framerate,
        }

    def _parse_and_load(self, d: dict):
        """
            Parses json formatted settings data, and loads it.
        """
        adaptive = d['resolution'] == 'adaptive'

        self.display = d['display']
        self.adaptive_resolution = adaptive,
        self.resolution = None if adaptive else tuple[int, int](d['resolution'])
        self.vsync = d['vsync']
        self.fullscreen = d['fullscreen']
        self.framerate = d['framerate']

    def _check_settings(self):
        """
            Checks for invalid game settings, warns, then sets to safe values.

            Invalid if:
            
            chosen display does not exist,
            resolution is not set while adaptive resolution is off,
            vsync is an invalid value,
            vsync is on but fullscreen isn't,
            framerate is not positive,

            Warns but does not fix if:
            resolution is an unusual value.
        """
        displays = pygame.display.get_desktop_sizes()

        # display
        if self.display >= len(displays) or self.display < 0:
            warnings.warn(f'Display is set to invalid value of {self.display} (there are {len(displays)} displays available). Defaulting to display 0...')
            self.display = 0

        # resolution
        if self.resolution is None:
            if not self.adaptive_resolution:
                warnings.warn('Non-adaptive resolution is "None". Making it adaptive...')
                self.adaptive_resolution = True
        else:
            if self.resolution[0] < 0 or self.resolution[1] < 0:
                warnings.warn('Resolution has negative values. Setting it to default of 1280x720...')
                self.resolution = RESOLUTIONS['1280x720']
            if self.resolution not in RESOLUTIONS.values():
                warnings.warn(f'Resolution is set to unusual value of {self.resolution[0]}x{self.resolution[1]}.')
                print(self.resolution)

        # vsync & fullscreen
        if self.vsync not in [-1, 0, 1]:
            warnings.warn('Vsync set to invalid value. Setting it to 0...')
            self.vsync = 0
        if self.vsync and not self.fullscreen:
            warnings.warn('Vsync is on but fullscreen is not. Turning fullscreen on...')
            self.fullscreen = True

        # framerate
        if self.framerate < 0.0:
            warnings.warn('Framerate is an impossible value. Setting to default of 60...')
            self.framerate = 60.0

    def build_flags(self):
        flags = 0
        if self.fullscreen:
            flags |= pygame.FULLSCREEN | pygame.SCALED
        if self.vsync:
            flags |= pygame.SCALED
        return flags

    def set_resolution(self):
        displays = pygame.display.get_desktop_sizes()
        if self.adaptive_resolution:
            self.resolution = displays[self.display]

    def save(self):
        with open(SAVE_LOCATION, 'w') as file:
            json.dump(self._as_dict(), file, indent=4)

    def load_and_sync(self):
        '''
            Loads values from SAVE_LOCATION, fixes bad values, then saves back to file.
        '''
        try:
            with open(SAVE_LOCATION, 'r') as file:
                self._parse_and_load(json.load(file))
        except json.JSONDecodeError:
            warnings.warn('Json failed to decode. Overwriting save with defaults...')
        except FileNotFoundError:
            warnings.warn(f'{SAVE_LOCATION} does not exist. Creating it now with default settings...')
            os.makedirs(SAVE_LOCATION, exist_ok=True)

        self._check_settings()
        self.set_resolution()
        self.save()

# test saving and loading
if __name__ == "__main__":
    # Settings should be set to defaults and a new directory called "saves/" should be created if it doesn't exist.
    # Data should be stored in SAVE_LOCATION
    import time
    pygame.init()
    settings = Settings()
    pygame.display.set_mode(settings.resolution)
    print('Saved initial settings!')
    time.sleep(5)
    # Change settings data. It should save to the save file
    settings.adaptive_resolution = False
    settings.resolution = RESOLUTIONS['1280x720']
    settings.fullscreen = False
    settings.save()
    print('Saved new settings!')
    pygame.quit()
