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
import shared
from copy import deepcopy
from constants import *
pygame.init()


class ContextCompare:
    def __init__(self, attrs):
        self.attrs = attrs
        self.prev = {a: None for a in attrs}

    def compare(self, obj):
        """
        Returns whether they are a match.
        """
        for a in self.attrs:
            if self.prev[a] != getattr(obj, a):
                return False
        return True

    def update(self, obj):
        for a in self.attrs:
            self.prev[a] = deepcopy(getattr(obj, a))


class Cursor:
    def __init__(self):
        pygame.mouse.set_visible(False)
        self.cursor = "NORMAL"

    def set_cursor(self, name):
        if name in CURSORS:
            self.cursor = name
        else:
            raise KeyError(f"{name} not in cursors.")


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


def bounds(val, v_min=0, v_max=1):
    return max(min(val, v_max), v_min)

def report_color(type):
    if type == "INFO":
        return REPORT_INFO
    elif type == "WARNING":
        return REPORT_WARNING
    elif type == "ERROR":
        return REPORT_ERROR
    else:
        raise ValueError(f"Invalid report type: {type}")


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

def cursor_wrap(loc, size, margin):
    nx, ny = shared.mouse_pos
    if shared.mouse_pos[0] <= loc[0]+margin:
        nx = size[0]
    elif shared.mouse_pos[0] >= size[0]+loc[0]-margin:
        nx = loc[0] + margin
    if shared.mouse_pos[1] <= loc[1]+margin:
        ny = size[1]
    elif shared.mouse_pos[1] >= size[1]+loc[1]-margin:
        ny = loc[1] + margin
    if nx != shared.mouse_pos[0] or ny != shared.mouse_pos[1]:
        pygame.mouse.set_pos(nx, ny)

def cursor_inside(loc, size):
    return loc[0] <= shared.mouse_pos[0] <= loc[0]+size[0] and loc[1] <= shared.mouse_pos[1] <= loc[1]+size[1]
