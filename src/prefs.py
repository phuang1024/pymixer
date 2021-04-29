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

import os
import time
import threading
import json
from constants import *


class Preferences:
    def __init__(self):
        if not os.path.isfile(PREFS_PATH):
            self.dump({})

        self.queue = []
        threading.Thread(target=self.queue_process).start()

    def queue_process(self):
        while get_run():
            time.sleep(0.05)

    def dump(self, data):
        with open(PREFS_PATH, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        with open(PREFS_PATH, "r") as file:
            return json.load(file)
