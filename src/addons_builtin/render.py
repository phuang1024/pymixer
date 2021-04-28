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

import vpy
from vpy.types import PropertyGroup, Operator
from vpy.types import BoolProp, IntProp


class RENDER_PT_Output(PropertyGroup):
    idname = "output"

    x_res = IntProp(
        name="X Resolution",
        description="Output X resolution in pixels.",
        default=1920, min=0, max=100000,
    )

    y_res = IntProp(
        name="Y Resolution",
        description="Output Y resolution in pixels.",
        default=1080, min=0, max=100000,
    )

    fps = IntProp(
        name="FPS",
        description="Output frames per second.",
        default=30, min=1, max=240,
    )

    frame_start: IntProp(
        name="Frame Start",
        description="Starting frame (inclusive) of animation.",
        default=0, min=0, max=100000,
    )

    frame_end: IntProp(
        name="Frame End",
        description="Ending frame (inclusive) of animation.",
        default=0, min=0, max=100000,
    )

    frame_current: IntProp(
        name="Current Frame",
        description="Current frame of animation.",
        default=0, min=0, max=100000,
    )


classes = (
    RENDER_PT_Output,
)

def register():
    for cls in classes:
        vpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        vpy.utils.unregister_class(cls)
