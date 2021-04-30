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

import pygame
import shared
from constants import *
from gui_utils import *


class Properties:
    attrs = (
        "draw_size",
        "draw_loc",
    )

    def __init__(self):
        self.context = ContextCompare(self.attrs)

    def draw(self, surface, loc, size):
        self.draw_size = size
        self.draw_loc = loc

        if not self.context.compare(self):
            pygame.draw.rect(surface, BLACK, (*loc, *size))

        self.context.update(self)
