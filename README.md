# ctftime_ics
Generate an ics file with CTFtime upcoming events. The calendar is created
based on the input parameters; if the output file already
exists, the program writes in append mode.

# Install
There is a __requirements.txt__ file which contains the list of all the needed
dependencies.

So

```
pip install requirements.txt
```

should be enough.


# Usage

The script uses CTF time api to get information about the upcoming CTF events.
You can specifiy some input parameters, which are listed below

* `-d`, `--days` (__mandatory__): the script reports information about events in
  a given __time window__. Such window is calculated as __last\_day__
- __today__, so the `-d` is used to specify which is the __last\_day__ to
  consider (e.g. -d 14 will fetch all the future event _within the next 14 days
from today_);

* `-w`, `--weight` (__optional__): ctfs usually have weights, which are a way
  to give an idea of the complexity and skills required for the challenges that
will be proposed. With this flag, you can filter all the events that have
a weight which is _less or equal_ to the given input weight

* `-o`, `--output` (__optional__): the output `ics` file name. This file will
  be created in your current directory, and by default the name is
__calendar.ics__. If you wish to change it, just use the `-o` flag. 

# Contribute

Contributions are warmly welcomed, if you have any new idea, have something
to add or find any kind of bug, feel free to open an issue/pull request.

# Roadmap

- Integrate the script with some sort of discord bot
