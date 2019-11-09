#!/bin/env python3

# https://pypi.org/project/exchangelib/

# https://stackoverflow.com/a/46649097/1386750
from exchangelib import DELEGATE, Account, Credentials, Configuration, EWSDateTime, EWSTimeZone
from configparser import RawConfigParser
import os

# Read the config file:
timezoneLocation = os.getenv('TZ', 'UTC')
config = RawConfigParser({
    'username':       '',
    'email_address':  '',
    'password':       '',
    'timezone':       '',
    'days_past':      7,
    'days_future':    30,
    'max_items':      100,
    'output_file':    'myCalendar.org',
    'calendar_name':  'My calendar',
    'orgmode_labels': ':Org:ews2cal:'  # Org mode labels
})
dir = os.path.dirname(os.path.realpath(__file__))
config.read(os.path.join(dir, 'config.cfg'))

server        = config.get(   'ews2org', 'server')
username      = config.get(   'ews2org', 'username')
emailAddrsss  = config.get(   'ews2org', 'email_address')
password      = config.get(   'ews2org', 'password')
timezone      = config.get(   'ews2org', 'timezone')
daysPast      = config.getint('ews2org', 'days_past')
daysFuture    = config.getint('ews2org', 'days_future')
maxItems      = config.getint('ews2org', 'max_items')
outFileName   = config.get(   'ews2org', 'output_file')
calName       = config.get(   'ews2org', 'calendar_name')
orgLabels     = config.get(   'ews2org', 'orgmode_labels')

print("server",        server)
print("username",      username)
print("email",         emailAddrsss)
print("password",      password)
print("timezone",      timezone)
print("daysPast",      daysPast)
print("daysFuture",    daysFuture)
print("maxItems",      maxItems)
print("outFileName",   outFileName)
print("calName",       calName)
print("orgLabels",     orgLabels)
print()

#exit(0)

# Set up account:
creds = Credentials(
    username=username,
    password=password
)

config = Configuration(server=server, credentials=creds)

account = Account(
    primary_smtp_address=emailAddrsss,
    autodiscover=False, 
    config=config,
    access_type=DELEGATE
)



startTime = account.default_timezone.localize(EWSDateTime(2019, 11, 7))
endTime = account.default_timezone.localize(EWSDateTime(2019, 11, 8))

if timezone=='':
    tz = EWSTimeZone.localzone()
else:
    tz = EWSTimeZone.timezone(timezone)


# # Line-ending replacement strings:
# # https://stackoverflow.com/a/43678795/1386750
# WINDOWS_LINE_ENDING = b'\r\n'
# UNIX_LINE_ENDING = b'\n'


# Open output file and write header line with calendar name and orgmode labels:
outFile = open(outFileName, 'w')
outFile.write('* '+calName+'  '+orgLabels+'\n')

INDENT=''
items = account.calendar.view(start=startTime, end=endTime, max_items=maxItems)
for item in items:
    item_start = EWSDateTime.astimezone(item.start,tz)
    item_end = EWSDateTime.astimezone(item.end,tz)
    #print(item_start.date(), item_start.time(), item_end.time(), item.subject, item.location)
    
    outFile.write('\n** '+item.subject+'\n')
    outFile.write(INDENT+'SCHEDULED '+item_start.strftime('<%Y-%m-%d %a %H:%M-')+item_end.strftime('%H:%M>\n'))
    if(item.text_body != None):
        content = str(item.text_body.strip()+'\n')
        #print(type(content))
        #content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        outFile.write(content)
    elif(item.body != None):
        outFile.write(item.body.strip()+'\n')
    
    outFile.write(INDENT+':PROPERTIES:\n')
    
    # People:
    if(item.organizer != None):
        outFile.write(INDENT+':ORGANISER:  '+item.organizer.name+' <'+item.organizer.email_address+'>\n')
        
    if(item.required_attendees != None):
        #outFile.write(INDENT+':ATTENDEES:  '+str(item.required_attendees)+'\n')
        outFile.write(INDENT+':ATTENDEES:\n')
        for att in item.required_attendees:
            outFile.write(INDENT+'  :ATTENDEE:   '+att.mailbox.name+' ('+att.response_type+')\n')
            
    
    if(item.optional_attendees != None):
        #outFile.write(INDENT+':ATTENDEES:  '+str(item.optional_attendees)+'\n')
        outFile.write(INDENT+':ATTENDEES:\n')
        for att in item.optional_attendees:
            outFile.write(INDENT+'  :ATTENDEE:   '+att.mailbox.name+' ('+att.response_type+')\n')
            
    
    # Metadata:
    if(item.my_response_type != None):
        outFile.write(INDENT+':RESPONSE:   '+str(item.my_response_type)+'\n')
    
    if(item.importance != None):
        outFile.write(INDENT+':PRIORITY:   '+str(item.importance)+'\n')
        
    if(item.is_cancelled != None):
        outFile.write(INDENT+':CANCELLED:  '+str(item.is_cancelled)+'\n')
        
    if(item.categories != None):
        #outFile.write(INDENT+':CATEGORIES: '+str(item.categories)+'\n')
        outFile.write(INDENT+':CATEGORIES:')
        for cat in item.categories:
            outFile.write(cat)
        outFile.write('\n')
        
    if(item.conflicting_meeting_count != None):
        outFile.write(INDENT+':CONFLICTS:  '+str(item.conflicting_meeting_count)+'\n')
        
    if(item.adjacent_meeting_count != None):
        outFile.write(INDENT+':ADJACENT:   '+str(item.adjacent_meeting_count)+'\n')
        
    if(item.is_recurring != None):
        outFile.write(INDENT+':RECURRING:  '+str(item.is_recurring)+'\n')
        
        if(item.recurrence != None):
            outFile.write(INDENT+'  :RECURRENCE: '+str(item.recurrence)+'\n')
        
        if(item.first_occurrence != None):
            outFile.write(INDENT+':FIRST OCCURRENCE: '+str(item.first_occurrence)+'\n')
        
        if(item.last_occurrence != None):
            outFile.write(INDENT+':LAST OCCURRENCE: '+str(item.last_occurrence)+'\n')

    
    if(item.headers != None):
        outFile.write(INDENT+':HEADERS:    '+str(item.headers)+'\n')
        
    if(item.datetime_created != None):
        outFile.write(INDENT+':CREATED:     '+item.datetime_created.strftime('[%Y-%m-%d %a %H:%M] \n'))
        
    if(item.web_client_read_form_query_string != None):
        outFile.write(INDENT+':LINK:        [['+item.web_client_read_form_query_string+'][Outlook]] \n')
        
    if(item.web_client_edit_form_query_string != None):
        outFile.write(INDENT+':LINK:        [['+item.web_client_edit_form_query_string+'][Outlook edit]] \n')
    
    # if(item.XXX != None):
    #     outFile.write(INDENT+':XXX: '+str(item.XXX)+'\n')
    
    outFile.write(INDENT+':END:\n')
    
outFile.close()
    
