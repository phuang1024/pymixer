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
import vpy
import shared
from constants import *
from gui_utils import ContextCompare, cursor_inside, cursor_wrap, draw_dashed_line
pygame.init()


class Preview:
    attrs = (
        "size",
        "loc",
        "draw_size",
        "draw_loc",
        "dragging",
        "drag_start_pos",
        "drag_start_loc",
    )

    def __init__(self):
        self.context = ContextCompare(self.attrs)

        self.draw_size = None
        self.draw_loc = None

        self.size = 540
        self.loc = [0, 0]

        self.dragging = False         # Whether currently dragging
        self.drag_start_pos = None    # Mouse position at start of drag
        self.drag_start_loc = None    # Preview position at start of drag

    def draw(self, surface, loc, size):
        self.draw_size = size
        self.draw_loc = loc

        # Check events
        if cursor_inside(loc, size):
            for event in shared.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        self.drag_start_pos = shared.mouse_pos
                        self.drag_start_loc = self.loc[:]
                    elif event.button == 4:
                        self.size *= 1.08
                    elif event.button == 5:
                        self.size /= 1.08

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_HOME and not self.dragging:
                        self.loc = [0, 0]
                        self.size = 540

            self.dragging = shared.mouse_pressed[1]
            if self.dragging:
                # Set new location
                self.loc = [
                    shared.mouse_pos[0] - self.drag_start_pos[0] + self.drag_start_loc[0],
                    shared.mouse_pos[1] - self.drag_start_pos[1] + self.drag_start_loc[1],
                ]

                # Cursor wrapping
                # cursor_wrap(loc, size, 5)

        if not self.context.compare(self):
            # Draw grid
            pygame.draw.rect(surface, BLACK, (*loc, *size))

            surf = pygame.Surface(size, pygame.SRCALPHA)
            x_center = loc[0] + size[0]/2
            y_center = loc[1] + size[1]/2

            width = self.size
            height = width / vpy.context.scene.output.x_res.get() * vpy.context.scene.output.y_res.get()
            x = x_center + self.loc[0] - width/2
            y = y_center + self.loc[1] - height/2

            draw_dashed_line(surf, (x, y), (x+width, y), 6, GRAY, 1)
            draw_dashed_line(surf, (x, y+height), (x+width, y+height), 6, GRAY, 1)
            draw_dashed_line(surf, (x, y), (x, y+height), 6, GRAY, 1)
            draw_dashed_line(surf, (x+width, y), (x+width, y+height), 6, GRAY, 1)

            surface.blit(surf, loc)

        self.context.update(self)
