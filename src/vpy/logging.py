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

RESET =  "\x1b[39m"
RED =    "\x1b[31m"
YELLOW = "\x1b[33m"
CYAN =   "\x1b[36m"


def info(msg, type_notice=True):
    sys.stdout.write(CYAN)
    if type_notice:
        sys.stdout.write("INFO: ")
    sys.stdout.write(msg+"\n")
    sys.stdout.write(RESET)


def warning(msg, type_notice=True):
    sys.stdout.write(YELLOW)
    if type_notice:
        sys.stdout.write("WARNING: ")
    sys.stdout.write(msg+"\n")
    sys.stdout.write(RESET)


def error(msg, type_notice=True):
    sys.stdout.write(RED)
    if type_notice:
        sys.stdout.write("ERROR: ")
    sys.stdout.write(msg+"\n")
    sys.stdout.write(RESET)
