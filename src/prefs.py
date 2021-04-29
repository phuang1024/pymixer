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
    #TODO write time into lock, and override when time is too old
    # to prevent lock staying when exiting abnormally.

    def __init__(self, path, lock_path):
        self.path = path
        self.lock_path = lock_path
        if not os.path.isfile(self.path):
            self.dump({})

        self.queue = []
        self.cache = {}
        threading.Thread(target=self.queue_process).start()

    def get(self, attr):
        if attr in self.cache:
            return self.cache[attr]
        else:
            val = self.load()[attr]
            self.cache[attr] = val
            return val

    def set(self, attr, val):
        self.queue.append((attr, val))

    def queue_process(self):
        while get_run():
            time.sleep(0.05)
            if len(self.queue) > 0:
                key, val = self.queue.pop(0)
                self.cache[key] = val

                data = self.load()
                data[key] = val
                self.dump(data)

    def dump(self, data):
        # while os.path.isfile(self.lock_path):
        #     time.sleep(0.01)
        # with open(self.lock_path, "w") as file:
        #     pass
        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)
        # os.remove(self.lock_path)

    def load(self):
        # while os.path.isfile(self.lock_path):
        #     time.sleep(0.01)
        # with open(self.lock_path, "w") as file:
        #     pass
        with open(self.path, "r") as file:
            # os.remove(self.lock_path)
            return json.load(file)
