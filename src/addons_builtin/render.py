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
from vpy.types import PropertyGroup, Operator, Context, Scene
from vpy.props import BoolProp, IntProp, EnumProp
pygame.init()


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

    frame_step: IntProp(
        name="Frame Step",
        description="Increment of frames.",
        default=1, min=1, max=240
    )

    frame_current: IntProp(
        name="Current Frame",
        description="Current frame of animation.",
        default=0, min=0, max=100000,
    )

    format: EnumProp(
        name="Output Format",
        description="Format of output, eg image type, video type, ...",
        items=(
            ("I1", "JPEG", "Output in .jpg image format."),
            ("I2", "PNG", "Output in .png image format."),
            ("I3", "TIFF", "Output in .tif image format."),
            ("V1", "MP4", "Output in .mp4 video format."),
            ("V2", "MOV", "Output in .mov video format."),
        )
    )


class RENDER_OT_RenderImage(Operator):
    name = "Render Image"
    description = "Render current frame and save to vpy.context.render_result"
    idname = "render.render_image"

    def poll(self, context: Context, *args, **kwargs):
        return isinstance(context.scene, Scene)

    def execute(self, context: Context, *args, **kwargs):
        # TODO render image
        context.render_result = vpy.utils.surf_to_array(pygame.Surface((1280, 720)))
        return "FINISHED"


class RENDER_OT_SaveImage(Operator):
    name = "Save Image"
    description = "Save image as a file."
    idname = "render.save_image"

    def poll(self, context: Context, *args, **kwargs) -> bool:
        return context.render_result is not None

    def execute(self, context: Context, *args, **kwargs) -> str:
        if "path" not in kwargs:
            self.report("ERROR", "Did not give path argument.")
            return "CANCELLED"

        pygame.image.save(vpy.utils.array_to_surf(context.render_result), kwargs["path"])
        return "FINISHED"


classes = (
    RENDER_PT_Output,
    RENDER_OT_RenderImage,
    RENDER_OT_SaveImage,
)

def register():
    for cls in classes:
        vpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        vpy.utils.unregister_class(cls)
