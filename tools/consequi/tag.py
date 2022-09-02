import time

from settings import *

class Tag:
    def __init__(self, name='', created=None, modified=None):
        current_time = round(time.time())
        self.name = name
        self.color = None
        self.parent = None

        if created:
            self.created = created
        else:
            self.created = current_time

        if modified:
            self.modified = modified
        else:
            self.modified = current_time
    def as_dict(self, compressed=True):
        task_dict = {}
        # If 'compressed' is set to True, use the abbreviated tag properties (as listed in settings)
        if compressed:
            for i, prop in enumerate(Settings.tag_properties):
                # Abbreviated attribute name
                short = Settings.tag_props_short[i]
                # Only add the property if this tag has it
                if hasattr(self, prop):
                    # print(prop)
                    task_dict[short] = getattr(self, prop)
        else:
            for i, prop in enumerate(Settings.tag_properties):
                short = Settings.tag_props_short[i]
                if hasattr(self, prop):
                    task_dict[prop] = getattr(self, prop)
        return task_dict
    def stringify(self, compressed=True):
        # Get dictionary and convert to a string, then return
        return json.dump(self.as_dict(compressed))
    def from_dict(self, data, compressed=True):
        if compressed:
            for i, prop in enumerate(Settings.tag_properties):
                short = Settings.tag_props_short[i]
                # if hasattr(data, short):
                if short in data:
                    setattr(self, prop, data[short])
        else:
            pass

        return self
