#
#  Video Editor
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


def write_addon_paths(paths):
    with open(ADDON_PATHS_FILE, "w") as file:
        file.write("\n".join(paths))


PARENT = os.path.dirname(os.path.realpath(__file__))
MODULE_PATH = os.path.join(PARENT, "vpy")
ADDON_PATHS_FILE = os.path.join(PARENT, "addon_paths.txt")

if os.path.isfile(ADDON_PATHS_FILE):
    with open(ADDON_PATHS_FILE, "r") as file:
        ADDON_PATHS = [l for l in file.read().strip().split() if not l.startswith("#")]
else:
    ADDON_PATHS = (
        os.path.join(PARENT, "addons_builtin"),
        os.path.join(PARENT, "addons_installed"),
    )
    write_addon_paths(ADDON_PATHS)

INIT_WIDTH = 1280
INIT_HEIGHT = 720
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
