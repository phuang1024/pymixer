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

import os
import pygame
pygame.init()


def get_run():
    return run

def set_run(val):
    global run
    run = val


PARENT = os.path.dirname(os.path.realpath(__file__))
PREFS_PATH = os.path.join(PARENT, "settings.json")
PREFS_LOCK_PATH = os.path.join(PARENT, "settings.lock")
MODULE_PATH = os.path.join(PARENT, "vpy")
ADDON_PATHS = (
    os.path.join(PARENT, "addons_builtin"),
    os.path.join(PARENT, "addons_installed"),
)

CURSORS = {
    "NORMAL": ["cursor_normal.jpg", None, (13, 6)],
    "HORIZONTAL": ["cursor_horizontal-arrow.jpg", None, (24, 24)],
    "VERTICAL": ["cursor_vertical-arrow.jpg", None, (24, 24)],
}

INIT_WIDTH = 1280
INIT_HEIGHT = 720
FPS = 60

BLACK = (0, 0, 0)
GRAY_DARK = (64, 64, 64)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
WHITE = (255, 255, 255)

REPORT_INFO = (80, 110, 170)
REPORT_WARNING = (190, 150, 90)
REPORT_ERROR = (180, 60, 60)

FONT_SMALL = pygame.font.SysFont("ubuntu", 14)
FONT_MED = pygame.font.SysFont("ubuntu", 28)
FONT_LARGE = pygame.font.SysFont("ubuntu", 48)

run = True


for i in CURSORS:
    path = os.path.join(PARENT, "assets", CURSORS[i][0])
    img = pygame.image.load(path)
    CURSORS[i][1] = img
