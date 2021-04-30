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
from prefs import Preferences
from ui.preview import Preview
from ui.sequencer import Sequencer
pygame.init()


class WindowManager:
    drag_margin = 5

    def __init__(self, prefs: Preferences):
        self.prefs = prefs
        if not prefs.has("layout.verticalsep"):
            prefs.set("layout.verticalsep", 0.8)
        if not prefs.has("layout.horizontalsep"):
            prefs.set("layout.horizontalsep", 0.5)

        self.preview = Preview()
        self.sequencer = Sequencer()
        # self.cursor = Cursor()

        self.dragging = 0    # bit 0 = dragging vertical, bit 1 = dragging horizontal
        self.x_sep = self.prefs.get("layout.verticalsep")
        self.y_sep = self.prefs.get("layout.horizontalsep")

    def draw(self, surface):
        width, height = surface.get_size()
        x_sep = self.x_sep*width
        y_sep = self.y_sep*height

        # Grid resize
        if shared.mouse_pressed[0]:
            margin = self.drag_margin

            # Drag vertical separator
            if (shared.mouse_event_1 and x_sep-margin<=shared.mouse_pos[0]<=x_sep+margin) or self.dragging&1:
                self.dragging |= 1
                self.x_sep = shared.mouse_pos[0]/width

            # Drag horizontal separator
            if (shared.mouse_event_1 and y_sep-margin<=shared.mouse_pos[1]<=y_sep+margin and
                    shared.mouse_pos[0]<=x_sep+margin) or self.dragging&2:
                self.dragging |= 2
                self.y_sep = shared.mouse_pos[1]/height

        else:
            if self.dragging != 0:
                self.prefs.set("layout.verticalsep", self.x_sep)
                self.prefs.set("layout.horizontalsep", self.y_sep)
            self.dragging = 0

        # Preview
        loc = (0, 0)
        size = (x_sep, y_sep)
        self.preview.draw(surface, loc, size)

        # Sequencer
        loc = (0, y_sep)
        size = (x_sep, height-y_sep)
        self.sequencer.draw(surface, loc, size)

        # Window separating grid
        pygame.draw.line(surface, GRAY_DARK, (0, y_sep), (x_sep, y_sep), 2)
        pygame.draw.line(surface, GRAY_DARK, (x_sep, 0), (x_sep, height), 2)
