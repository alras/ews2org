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


# ### MAIN ###

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
        duration = 0
        if(startTime is not None and endTime is not None): duration = endTime.dt - startTime.dt
        
        if(startTime is not None):
            if(duration.days > 1):
                print(colored('Start date:  ', 'green', attrs=['bold']), startTime.dt.strftime('%A %d %B %Y (week %V)'))
            else:
                print(colored('Date:        ', 'green', attrs=['bold']), startTime.dt.strftime('%A %d %B %Y (week %V)'))
            print(colored('Start time:  ', 'green', attrs=['bold']), startTime.dt.strftime('%H:%M %Z'))
        elif(endTime is not None):
            print(colored('Date:        ', 'green', attrs=['bold']), endTime.dt.strftime('%A %d %B %Y (week %V)'))
        if(endTime is not None):
            if(duration.days > 1):
                print(colored('End date:    ', 'green', attrs=['bold']), endTime.dt.strftime('%A %d %B %Y (week %V)'))
            print(colored('End time:    ', 'green', attrs=['bold']), endTime.dt.strftime('%H:%M %Z'))
        if(startTime is not None and endTime is not None):
            if(duration.days > 1):
                print(colored('Duration:    ', 'green', attrs=['bold']), strfdelta(endTime.dt - startTime.dt, "%D days, %H:%M"))
            else:
                print(colored('Duration:    ', 'green', attrs=['bold']), strfdelta(endTime.dt - startTime.dt, "%H:%M"))
        print()
        
        
        # Location:
        location = component.get('location')
        if(location != '' and location is not None):
            print(colored('Location:    ', 'green', attrs=['bold']), component.get('location'))
            print()
        
        # Organiser and attendees:
        organiser = component.get('organizer')
        if(type(organiser) == str):  # Can only .replace() on string
            print(colored('Organiser:   ', 'green', attrs=['bold']), organiser.replace('MAILTO:',''))
        elif(organiser is not None):
            print(colored('Organiser:   ', 'green', attrs=['bold']), organiser)
            
        count = 0
        attendees = component.get('attendee')
        if(attendees is not None):
            if(type(attendees) == list):
                for attendee in attendees:
                    count +=1 
                    if(type(attendee) == str):  # Can only .replace() on string
                        print(colored('Attendee '+str(count)+':    ', 'green', attrs=['bold']), attendee.replace('MAILTO:',''))
                    else:
                        print(colored('Attendee '+str(count)+':    ', 'green', attrs=['bold']), attendee)
            else:  # if(type(attendees) == (icalendar.Calendar.)prop.vCalAddress), probably == single attendee:
                if(type(attendees) == str):  # Can only .replace() on string
                    print(colored('Attendee:    ', 'green', attrs=['bold']), attendees.replace('MAILTO:',''))
                else:
                    print(colored('Attendee:    ', 'green', attrs=['bold']), attendees)
                    
        # Creation date:
        created = component.get('dtstamp')
        if(created is not None):
            print()
            print(colored('Created:     ', 'green', attrs=['bold']), created.dt.strftime('%A %d %B %Y, %H:%M:%S %Z'))
        
print()
