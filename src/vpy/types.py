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


class Scene:
    meta: bytes
    is_saved: bool
    is_dirty: bool

    frame_start: int
    frame_end: int
    frame_step: int
    fps: int

    def __init__(self, **kwargs) -> None:
        self.meta = b""
        self.is_saved = False
        self.is_dirty = False

        self.frame_start = 0
        self.frame_end = 600
        self.frame_step = 1
        self.fps = 30

        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])


class Operator:
    label: str
    description: str
    idname: str

    def __call__(self, scene: Scene) -> str:
        if self.poll(scene):
            return self.execute(scene)
        else:
            return "CANCELLED"

    def poll(self, scene: Scene) -> bool:
        """
        The operator should return a bool based on the scene,
        specifying whether requirements, if any, are met (eg scene.fps >= 30)
        """
        return True

    def execute(self, scene: Scene) -> str:
        """
        This function is called when the operator is called,
        usually by the user pressing a button in the GUI.
        The return values of this function should be "FINISHED" or "CANCELLED"
        :param scene: The scene during when the operator is executed.
        """
        return "FINISHED"
