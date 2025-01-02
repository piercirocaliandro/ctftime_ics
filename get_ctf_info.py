import datetime
import time
import requests
from ics import Calendar, Event
import dateutil
import os
import argparse

class CtfCalendarEntry():
    '''
     Entry for the CTF calendar, holding the key information about it.
    '''
    def __init__(self, name, start, end, url, ctftime_url):
        self._name = name
        self._start = start
        self._end = end
        self._url = url
        self._ctftime_url = ctftime_url

    def __str__(self):
        return f'name: {self.name}, start: {self.start}, end: {end}, url: {self.url}, ctftime_url: {ctftime_url}'

    def get_name(self):
        return self._name

    def get_weight(self):
        return self._weight

    def get_url(self):
        return self._url
    
    def get_description(self):
        return f'For more info see: {self._ctftime_url}'

    def get_start_date(self):
        return self._get_time_local(self._start)

    def get_end_date(self):
        return self._get_time_local(self._end)

    def _get_time_local(self, src_date):
        '''
         Convert time from UTC (time format used by CTFtime) into local time.
         Return datetime in the format `%Y-%m-%d %H:%M`

         @param src_date Datetime as returned by CTFtime api
        '''
        src_date = dateutil.parser.parse(src_date)
        from_zone = dateutil.tz.tzutc()
        to_zone = dateutil.tz.tzlocal()
        src_date = src_date.replace(tzinfo=from_zone)
        central = src_date.astimezone(to_zone)

        return central.strftime("%Y-%m-%d %H:%M")

class CtfCalendar():
    def __init__(self, events, calendar_file="calendar.ics"):
        '''
         Class that represents a new ctf calendar. By default, if the user does
         not specify a file name, the calendar name will be 'calendar.ics'.

         @param events          `CtfCalendarEntry` list of entries
         @param calendar_file   Calendar file name
        '''
        self._events = events
        self._calendar_name = calendar_file

    def write_to_calendar(self):
        '''
         Write all the events to the calendar. If the calendar file already
         exists, write in append mode, else create a new file. 
        '''
        c = Calendar()
        for event in self._events:
            e = Event()

            e.name = event.get_name()
            e.begin = event.get_start_date()
            e.end = event.get_end_date()
            e.url = event.get_url()
            e.description = event.get_description()
            c.events.add(e)
        
        write_type = 'w'
        if os.path.exists(self._calendar_name):
            write_type = 'a'
        with open(self._calendar_name, write_type) as f:
            f.writelines(c.serialize_iter())
            c.serialize()

class CtfTimeApiReq():
    def __init__(self, days_window, max_weight):
        '''
         Use CTFtime API ("https://ctftime.org/api/") to retrieve information
         about events in a specific window of days (starting from the current
         date).
        '''
        self._url = "https://ctftime.org/api/v1/events/"
        self._days_window = days_window
        self._max_weight = max_weight

    def send_request(self):
        '''
         Send a request to CTFtime api and return the responde
        '''
        x = datetime.date.today()
        y = x + datetime.timedelta(self._days_window)
        x_u = int(time.mktime(x.timetuple()))
        y_u = int(time.mktime(y.timetuple()))
        
        params = {
                "limit": 100,
                "start": x_u,
                "finish": y_u
        }
        headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        return requests.get(self._url, params=params, headers=headers)

    def get_events(self):
        '''
         Return a list of `CtfCalendarEntry`, which are the ctf events that
         occur in the specified time window.
        '''
        r = self.send_request()
        if (r.status_code != 200):
            print("[X] Something went wrong!")
            exit(1)
        content = r.json()
        entries = []
        for ctf in content:
            weight = ctf['weight']
            ce = CtfCalendarEntry(ctf['title'], ctf['start'], ctf['finish'],
                                  ctf['url'], ctf['ctftime_url'])
            if self._max_weight == 0 or weight <= self._max_weight:
                entries.append(ce)
        return entries

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
            prog='get_ctf_info.py',
            description='Leverage CTFtime API to get info about future CTF events and export them as an ics file (to import in your favourite calendar application)',
            epilog='For more info, see https://ctftime.org/api/'
            )
    arg_parser.add_argument("-d", "--days", type=int, required=True,
                            help='Number of days for the time window')
    arg_parser.add_argument("-w", "--weight", type=float, default=0.00,
                            help='If > 0.0, only ctfs which weight is lower than the specified value are saved')
    arg_parser.add_argument("-o", "--output", type=str, help='Output calendar file name')
    args = arg_parser.parse_args()

    ctf = CtfTimeApiReq(args.days, args.weight)
    entries = ctf.get_events()
    if args.output is None:
        calendar = CtfCalendar(entries)
    else:
        calendar = CtfCalendar(entries, args.output+'.ics')
    calendar.write_to_calendar()
