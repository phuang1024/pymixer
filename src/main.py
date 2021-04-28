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
from constants import *

sys.path.insert(0, MODULE_PATH)
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from gui import gui
from addon_manager import addon_manager


def main():
    if len(sys.argv) >= 2:
        if sys.argv[1] in ("--help", "-h"):
            print("Pymixer - GNU GPL 3 license")
            print("Usage:")
            print("  -h, --help             Show this help menu")
            print("  -a, --addon-manager    Open the CLI addon manager")

        elif sys.argv[1] in ("-a", "--addon-manager"):
            addon_manager()

    else:
        gui()


main()
