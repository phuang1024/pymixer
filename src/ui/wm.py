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

import time
import pygame
import shared
from constants import *
from gui_utils import *
from prefs import Preferences
from ui.preview import Preview
from ui.properties import Properties
from ui.sequencer import Sequencer
pygame.init()


class WindowManager:
    drag_margin = 5
    status_bar_height = 28
    report_time = 10

    def __init__(self, prefs: Preferences):
        self.prefs = prefs
        if not prefs.has("ui.verticalsep"):
            prefs.set("ui.verticalsep", 0.8)
        if not prefs.has("ui.horizontalsep"):
            prefs.set("ui.horizontalsep", 0.5)

        self.preview = Preview()
        self.sequencer = Sequencer()
        self.properties = Properties()

        # self.cursor = Cursor()

        self.dragging = 0    # bit 0 = dragging vertical, bit 1 = dragging horizontal
        self.x_sep = self.prefs.get("ui.verticalsep")
        self.y_sep = self.prefs.get("ui.horizontalsep")

    def draw(self, surface):
        # Keyboard shortcuts for operators
        for event in shared.events:
            if event.type == pygame.KEYDOWN:
                if 0 <= event.key < 256:
                    key = chr(event.key)
                    shortcut = (key, shared.keys_shift, shared.keys_alt, shared.keys_ctrl)
                    idname = vpy.utils.shortcut_to_op(shortcut)
                    if idname is not None:
                        group, name = idname.split(".")
                        getattr(getattr(vpy.ops, group), name)()

        width, height = surface.get_size()
        height -= self.status_bar_height
        x_sep = self.x_sep*width
        y_sep = self.y_sep*height

        # Grid resize
        if shared.mouse_pressed[0]:
            margin = self.drag_margin

            # Drag vertical separator
            if (shared.mouse_event_1 and x_sep-margin<=shared.mouse_pos[0]<=x_sep+margin) or self.dragging&1:
                self.dragging |= 1
                self.x_sep = bounds(shared.mouse_pos[0]/width)

            # Drag horizontal separator
            if (shared.mouse_event_1 and y_sep-margin<=shared.mouse_pos[1]<=y_sep+margin and
                    shared.mouse_pos[0]<=x_sep+margin) or self.dragging&2:
                self.dragging |= 2
                self.y_sep = bounds(shared.mouse_pos[1]/height)

        else:
            if self.dragging != 0:
                self.prefs.set("ui.verticalsep", self.x_sep)
                self.prefs.set("ui.horizontalsep", self.y_sep)
            self.dragging = 0

        # Preview
        loc = (0, 0)
        size = (x_sep, y_sep)
        self.preview.draw(surface, loc, size)

        # Sequencer
        loc = (0, y_sep)
        size = (x_sep, height-y_sep)
        self.sequencer.draw(surface, loc, size)

        # Properties
        loc = (x_sep, 0)
        size = (width-x_sep, height)
        self.properties.draw(surface, loc, size)

        # Status bar
        pygame.draw.rect(surface, BLACK, (0, height, width, self.status_bar_height))
        if vpy.context.last_report is not None and vpy.context.last_report_time >= time.time()-self.report_time:
            report = vpy.context.last_report
            text = FONT_SMALL.render(report[0].capitalize()+": "+report[1], True, WHITE)
            w, h = text.get_size()

            text_x = width/2 - w/2
            text_y = height + self.status_bar_height/2 - h/2
            rect_coords = (text_x-3, text_y-2, w+6, h+4)
            pygame.draw.rect(surface, report_color(report[0]), rect_coords, border_radius=2)
            surface.blit(text, (text_x, text_y))

        # Window separating grid
        pygame.draw.line(surface, GRAY_DARK, (0, y_sep), (x_sep, y_sep), 2)
        pygame.draw.line(surface, GRAY_DARK, (x_sep, 0), (x_sep, height), 2)
        pygame.draw.line(surface, GRAY_DARK, (0, height), (width, height), 2)
