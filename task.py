import time
import uuid

import datetime
from recurrent.event_parser import RecurringEvent
from dateutil import rrule

from settings import *
from duration import *

class Task:
    def __init__(self, content='', name='', created=None, modified=None, datestring=None, importance=1000, durationstring=None):
        current_time = round(time.time())

        self.name = name
        self.content = content

        self.id = uuid.uuid4().hex

        if created:
            self.created = created
        else:
            self.created = current_time

        if modified:
            self.modified = modified
        else:
            self.modified = current_time

        # self.next = 1
        self.datestring = datestring

        if self.datestring != None and len(self.datestring) > 0:
            try:
                now = datetime.datetime.now()
                # now = datetime.datetime(2010, 1, 1)
                r = RecurringEvent(now_date=now)
                self.dateparse = r.parse(self.datestring)
                self.dateparams = r.get_params()
                self.datesummary = r.format(self.dateparse)
                if r.is_recurring:
                    rr = rrule.rrulestr(r.get_RFC_rrule())
                    self.next = str(rr.after(now))

                    print(self.dateparse, self.dateparams, self.datesummary, self.next)
            except Exception as e:
                print(e)

        self.durationstring = durationstring

        if self.durationstring != None and len(self.durationstring) > 0:
            self.duration = parse_duration(self.durationstring)

        self.importance = {
            'user_defined': importance,
            'calculated': 1000.,
            'history': [],
            'ranked': []
        }
        if hasattr(self, 'dateparse'):
            self.dateparse = str(self.dateparse)

    def update(self):
        if hasattr(self, 'duration') and hasattr(self, 'importance') and self.duration != 0:
            self.efficiency_ratio = self.importance['calculated'] / self.duration

    # there might be a bug here where some of the properties are misaligned with their values...

    # is name dict reserved?
    def as_dict(self, compressed=True):
        task_dict = {}
        # If 'compressed' is set to True, use the abbreviated task properties (as listed in settings)
        if compressed:
            for i, prop in enumerate(Settings.task_properties):
                # Abbreviated attribute name
                short = Settings.task_props_short[i]
                # Only add the property if this task has it
                if hasattr(self, prop):
                    # print(prop)
                    task_dict[short] = getattr(self, prop)
        else:
            for i, prop in enumerate(Settings.task_properties):
                short = Settings.task_props_short[i]
                if hasattr(self, prop):
                    task_dict[prop] = getattr(self, prop)
        return task_dict
    def stringify(self, compressed=True):
        # Get dictionary and convert to a string, then return
        return json.dump(self.as_dict(compressed))
    def from_dict(self, data, compressed=True):
        if compressed:
            for i, prop in enumerate(Settings.task_properties):
                short = Settings.task_props_short[i]
                # if hasattr(data, short):
                if short in data:
                    setattr(self, prop, data[short])
            # For backwards-compatibility, round existing calculated importance scores if they have extra precision
            try:
                self.importance['calculated'] = round(self.importance['calculated'])
            except:
                pass
        else:
            pass

        self.update()
        return self
