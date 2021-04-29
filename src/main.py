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
import argparse
from constants import *

sys.path.insert(0, MODULE_PATH)
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from gui import gui
from addon_manager import addon_manager
from cli import cli


def main():
    parser = argparse.ArgumentParser(description="Run Pymixer in different modes. Launch the GUI by providing no arguments.")
    parser.add_argument("-c", "--cli", help="send a command to the CLI interface", type=str)
    parser.add_argument("-a", "--addons", help="open the CLI addon manager", action="store_true")
    parser.add_argument("-g", "--gui", help="open the GUI (also works with no argument)", action="store_true")   # Added for completion
    args = parser.parse_args()

    if args.cli:
        cli(args.cli)
    elif args.addons:
        addon_manager()
    else:
        gui()


main()
