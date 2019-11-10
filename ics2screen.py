#!/bin/env python3

"""Read an ics (=vcs/vcal?) iCalendar file and print the most important contents to stdout.

See:
  - https://stackoverflow.com/a/3408488/1386750
  - http://lukasmartinelli.ch/python/2014/02/15/using-python-to-parse-icalendar-file.html

"""


# https://stackoverflow.com/a/8907269/1386750
from string import Template
class DeltaTemplate(Template):
    delimiter = "%"
def strfdelta(tdelta, fmt):
    """strftime() for timedelta."""
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    for label in ("H","M","S"):
        d[label] = "%2.2i" % (d[label])
    t = DeltaTemplate(fmt)
    return t.substitute(**d)



### MAIN ###

from icalendar import Calendar
from termcolor import colored
from sys import argv

# Get the file name:
if(len(argv) <= 1):
    print("Syntax: "+argv[0]+" <ics/vcs file>")
    exit(1)

inFile = argv[1]  # Should be ics?  Seems to work.


# Open the file and read it:
try:
    file = open(inFile, 'rb')
except Exception as e:
    print(e)
    exit(1)

cal = Calendar.from_ical(file.read())
file.close()


# Print the contents:
print("Contents of "+inFile+":")
for component in cal.walk():
    if component.name == "VEVENT":
        print()
        
        # Subject:
        print(colored('Summary:     ', 'green', attrs=['bold']), component.get('summary'))
        print()
        
        # Date and start and end time:
        startTime = component.get('dtstart')
        endTime = component.get('dtend')
        if(startTime != None):
            print(colored('Date:        ', 'green', attrs=['bold']), startTime.dt.strftime('%A %d %B %Y (week %V)'))
            print(colored('Start time:  ', 'green', attrs=['bold']), startTime.dt.strftime('%H:%M %Z'))
        elif(endTime != None):
            print(colored('Date:        ', 'green', attrs=['bold']), endTime.dt.strftime('%A %d %B %Y (week %V)'))
        if(endTime != None):
            print(colored('End time:    ', 'green', attrs=['bold']), endTime.dt.strftime('%H:%M %Z'))
        if(startTime != None and endTime != None):
            print(colored('Duration:    ', 'green', attrs=['bold']), strfdelta(endTime.dt - startTime.dt, "%H:%M"))
        print()
        
        # Location:
        print(colored('Location:    ', 'green', attrs=['bold']), component.get('location'))
        print()
        
        # Organiser and attendees:
        print(colored('Organiser:   ', 'green', attrs=['bold']), component.get('organizer').replace('MAILTO:',''))
        count = 0
        attendees = component.get('attendee')
        if(attendees != None):
            for attendee in attendees:
                count +=1 
                print(colored('Attendee '+str(count)+':    ', 'green', attrs=['bold']), attendee.replace('MAILTO:',''))
        
        # Creation date:
        created = component.get('dtstamp')
        if(created != None):
            print()
            print(colored('Created:     ', 'green', attrs=['bold']), created.dt.strftime('%A %d %B %Y, %H:%M:%S %Z'))
        
print()
