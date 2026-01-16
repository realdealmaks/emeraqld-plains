# connector
# this file is for storing data

import json
import os

# stores data in json

def connector(main_globals):
    default_data = {
            "music": 1.0, # *100 in %
            "max_fps": 120,
            "resolution": (1080, 750),
            "best_floor": 0,
            "most_groups_cleared": 0,
            "most_enemies_killed": 0,
            "richest_player": 0,
            "total_deaths": 0,
    }

    class Connector:
        def __init__(self, filename="data.json", default_data=None):
            self.filename = filename
            self.default_data = default_data or {}
            self.data = {}
            self.load_data()

        def get_data(self):
            return self.data

        def set_data(self, new_data):
            self.data = new_data

        def save_data(self):
            with open(self.filename, "w") as f:
                json.dump(self.data, f, indent=4)
            return self.data

        def load_data(self):
            if os.path.exists(self.filename):
                try:
                    with open(self.filename, "r") as f:
                        self.data = json.load(f)
                    # if file is empty
                    if not self.data:
                        self.data = self.default_data
                        self.save_data()
                except json.JSONDecodeError:
                    # if file is corrupt and goes against israel
                    self.data = self.default_data
                    self.save_data()
            else:
                # if file doesnt exist
                self.data = self.default_data
                self.save_data()
            return self.data

    main_globals['connector_instance'] = Connector(default_data=default_data)

    print("connector, ", end = "")

# test to see if the file gets written anything
test = False
if test:
    main_globals = {}
    connector(main_globals)
    print(main_globals['connector_instance'].get_data())