#!/bin/env python3

"""List today's meetings, or, if an integer argument is provided, N days from now."""

from exchangelib import DELEGATE, Account, Credentials, Configuration, EWSDateTime, EWSDate, EWSTimeZone
from datetime import timedelta
from configparser import RawConfigParser
from termcolor import colored
from sys import argv
import os


# Get the number of days w.r.t. today from the command line:
deltaDay = 0  # Default: today
if(len(argv) > 1):
    try:
        deltaDay = int(argv[1])
    except Exception as e:
        print(e)
        print("Syntax: "+argv[0]+" <number of days from today (int)>")
        exit(1)


# Read the config file:
config = RawConfigParser({
    'username':       '',
    'email_address':  '',
    'password':       '',
    'timezone':       '',
})
dir = os.path.dirname(os.path.realpath(__file__))
config.read(os.path.join(dir, 'ews2org.cfg'))

server        = config.get(   'ews2org',         'server')
username      = config.get(   'ews2org',       'username')
emailAddress  = config.get(   'ews2org',  'email_address')
password      = config.get(   'ews2org',       'password')
timezone      = config.get(   'ews2org',       'timezone')

# Check settings:
if False:
    print("server:      ",        server)
    print("username:    ",      username)
    print("email:       ",  emailAddress)
    print("password:    ",      password)
    print("timezone:    ",      timezone)
    print()
    

# Set up account:
creds = Credentials(
    username=username,
    password=password
)

config = Configuration(server=server, credentials=creds)

account = Account(
    primary_smtp_address=emailAddress,
    autodiscover=False, 
    config=config,
    access_type=DELEGATE
)


# Start and end date to fetch calendar items for:
today     = EWSDate.today() + timedelta(days=deltaDay)
startDate = account.default_timezone.localize(EWSDateTime(today.year, today.month, today.day,  0,  0,  0))
endDate   = account.default_timezone.localize(EWSDateTime(today.year, today.month, today.day, 23, 59, 59))


# Desired timezone:
if timezone=='':
    tz = EWSTimeZone.localzone()
else:
    tz = EWSTimeZone.timezone(timezone)


# Start output:
print()
print(colored('Appointments for '+startDate.strftime('%A %d %B %Y')+':', 'red',attrs=['bold','underline']))


# Remove warnings like: Cannot convert value '' on field '_start_timezone' to type <class 'exchangelib.ewsdatetime.EWSTimeZone'> (unknown timezone ID)
import sys
sys.stderr = open('/dev/null', 'w')

INDENT='              '
items = account.calendar.view(start=startDate, end=endDate)
count = 0
for item in items:
    count += 1
    
    item_start = EWSDateTime.astimezone(item.start, tz)  # Start time of item in the desired timezone
    item_end   = EWSDateTime.astimezone(item.end,   tz)  # End time of item in the desired timezone
    
    print()
    print(colored(item_start.strftime('%H:%M-')+item_end.strftime('%H:%M')+':  '+item.subject+':', 'white',
                      attrs=['underline', 'bold']))
    
    # People:
    if(item.organizer != None):
        print(INDENT+colored('Organiser:', 'green', attrs=['dark'])+'  '+item.organizer.name+' <'+item.organizer.email_address+'>')
        
    # Metadata:
    print(INDENT+colored('Location:', 'green', attrs=['dark'])+'   '+str(item.location))
    
    if(item.my_response_type != None):
        print(INDENT+colored('Response:', 'green', attrs=['dark'])+'   '+str(item.my_response_type))
    
    if(item.is_cancelled == True):
        print(INDENT+colored('Cancelled:  '+str(item.is_cancelled), 'red', attrs=['bold']))
        
    if(item.conflicting_meeting_count != 0):
        print(INDENT+colored('Conflicts:', 'red', attrs=['bold'])+'  '+str(item.conflicting_meeting_count))
        
    if(item.adjacent_meeting_count != 0):
        print(INDENT+colored('Adjacent:', 'yellow', attrs=['bold'])+'   '+str(item.adjacent_meeting_count))


# Report number of appointments found:
print()
if(count == 0):
    print("No appointments were found for this day.")
elif(count == 1):
    print("One appointment was found for this day.")
else:
    print(str(count)+" appointments were found for this day.")
print()
