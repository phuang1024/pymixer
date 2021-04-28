#
#  Pymixer
#  Video editor with a Python API.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
import os
import importlib
import pygame
import vpy
from constants import *
pygame.init()


def setup_api():
    register(ADDON_PATHS)
    vpy.context.scene = vpy.types.Scene()


def register(dirs):
    for d in dirs:
        if os.path.isdir(d):
            sys.path.append(d)
            for f in os.listdir(d):
                register_module(f)
            sys.path.pop()


def register_module(file):
    try:
        mod = importlib.import_module(os.path.splitext(file)[0])
        mod.register()
    except AttributeError:   # Tried to import __pycache__
        pass


def kmod(key, target_key, ctrl=False, shift=False, alt=False):
    keys = pygame.key.get_pressed()
    ctrl_pressed = (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])
    shift_pressed = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
    alt_pressed = (keys[pygame.K_LALT] or keys[pygame.K_RALT])

    meets_requires = True
    if ctrl != ctrl_pressed:
        meets_requires = False
    if shift != shift_pressed:
        meets_requires = False
    if alt != alt_pressed:
        meets_requires = False

    if meets_requires and key == target_key:
        return True
    return False


def draw_dashed_line(surface, start, end, dash_size, color, size):
    x, y = start
    ex, ey = end
    dist = (abs(x-ex)**2 + abs(y-ey)**2) ** 0.5
    steps = int(dist/dash_size) + 1
    dx = abs(x-ex) / steps
    dy = abs(y-ey) / steps

    for i in range(steps):
        if i % 2 == 0:
            dist_so_far = dash_size * (i+1)
            fac = min(dash_size, abs(dist-dist_so_far)) / dash_size
            pygame.draw.line(surface, color, (x, y), (x + dx*fac, y + dy*fac), size)

        x += dx
        y += dy
