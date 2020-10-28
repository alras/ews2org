#!/bin/env python3

"""Read an ics/ical (=vcs/vcal?) iCalendar file and write the most important contents to
  an emacs orgmode file with extension .org.

See:
  - https://stackoverflow.com/a/3408488/1386750
  - http://lukasmartinelli.ch/python/2014/02/15/using-python-to-parse-icalendar-file.html

"""

# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete
from icalendar import Calendar


def main():
    """Main function."""
    
    # Parse command-line arguments:
    parser = argparse.ArgumentParser(description="Convert an .ics or .vcs calendar file to an orgmode agenda file.", 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # Use capital, period, add default values
    
    # Required arguments:
    parser.add_argument("inFile", type=str, default=None, help=".ics or .vcs file name")
    
    # Optional arguments
    parser.add_argument("-q", "--quiet",   action="store_true", help="be quiet; produce no output")  # Default = False
    
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    
    
    # Open the input file and read it:
    inFile = args.inFile
    try:
        file = open(inFile, 'rb')
    except Exception as e:
        print(e)
        exit(1)
    
    cal = Calendar.from_ical(file.read())
    file.close()
    
    outFile = inFile.replace('.ics', '.org')
    outFile = outFile.replace('.vcs', '.org')
    if(outFile == inFile): outFile = inFile+".org"
    
    if(not args.quiet):
        print(inFile, outFile)
    
    
    # Open the outfile for writing:
    try:
        file = open(outFile, 'w')
    except Exception as e:
        print(e)
        exit(1)
    
    
    # Write the contents to file:
    file.write("* "+inFile+"\n")
    for component in cal.walk():
        if component.name == "VEVENT":
            props = False  # Is :PROPERTIES: present?
    
            file.write("\n")
    
            # Subject:
            file.write("** "+component.get('summary')+"\n")
    
            # Date and start and end time:
            startTime = component.get('dtstart')
            endTime   = component.get('dtend')
            if(startTime is not None):
                file.write(startTime.dt.strftime('<%Y-%m-%d %a '))
                file.write(startTime.dt.strftime('%H:%M'))
            elif(endTime is not None):
                file.write(endTime.dt.strftime('<%Y-%m-%d %a '))
            if(endTime is not None):
                if(startTime != endTime):
                    if(startTime is not None):
                        file.write('-')
                    file.write(endTime.dt.strftime('%H:%M'))
            file.write('>\n')
    
            # Location:
            location = component.get('location')
            if(location != '' and location is not None):
                if(not props):
                    file.write(":PROPERTIES:\n")
                    props = True
                file.write(':LOCATION:    '+component.get('location')+"\n")
    
            # Organiser and attendees:
            organiser = component.get('organizer')
            if(type(organiser) == str):  # Can only .replace() on string
                if(not props):
                    file.write(":PROPERTIES:\n")
                    props = True
                file.write(':ORGANISER:   '+organiser.replace('MAILTO:','')+"\n")
            elif(organiser is not None):
                if(not props):
                    file.write(":PROPERTIES:\n")
                    props = True
                file.write(':ORGANISER:   '+organiser+"\n")
    
            count = 0
            attendees = component.get('attendee')
            if(attendees is not None):
                if(type(attendees) == list):
                    for attendee in attendees:
                        count +=1 
                        if(type(attendee) == str):  # Can only .replace() on string
                            if(not props):
                                file.write(":PROPERTIES:\n")
                                props = True
                            file.write(':ATTENDEE '+str(count)+':    '+attendee.replace('MAILTO:','')+"\n")
                        else:
                            if(not props):
                                file.write(":PROPERTIES:\n")
                                props = True
                            file.write(':ATTENDEE '+str(count)+':    '+attendee+"\n")
                else:  # if(type(attendees) == (icalendar.Calendar.)prop.vCalAddress), probably == single attendee:
                    if(type(attendees) == str):  # Can only .replace() on string
                        if(not props):
                            file.write(":PROPERTIES:\n")
                            props = True
                        file.write(':ATTENDEE:    '+attendees.replace('MAILTO:','')+"\n")
                    else:
                        if(not props):
                            file.write(":PROPERTIES:\n")
                            props = True
                        file.write(':ATTENDEE:    '+attendees+"\n")
    
            # Creation date:
            created = component.get('dtstamp')
            if(created is not None):
                if(not props):
                    file.write(":PROPERTIES:\n")
                    props = True
                file.write(':CREATED:     '+created.dt.strftime('%A %d %B %Y, %H:%M:%S %Z')+"\n")
    
            if(props):
                file.write(":END:\n")
    return


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


if(__name__ == "__main__"): main()
