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


def get_run():
    return run

def set_run(val):
    global run
    run = val


PARENT = os.path.dirname(os.path.realpath(__file__))
PREFS_PATH = os.path.join(PARENT, "settings.json")
MODULE_PATH = os.path.join(PARENT, "vpy")
ADDON_PATHS = (
    os.path.join(PARENT, "addons_builtin"),
    os.path.join(PARENT, "addons_installed"),
)

INIT_WIDTH = 1280
INIT_HEIGHT = 720
FPS = 60

BLACK = (0, 0, 0)
GRAY_DARK = (64, 64, 64)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
WHITE = (255, 255, 255)

run = True
