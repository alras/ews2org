#!/bin/env python3

# https://pypi.org/project/exchangelib/

# https://stackoverflow.com/a/46649097/1386750
from exchangelib import EWSDateTime, EWSTimeZone
from datetime import timedelta

from ews2org import readConfigFile, setupAccount
import htmlstrip

# Read the config file:
server, username, emailAddress, password, timezone, daysPast, daysFuture, \
        maxItems, outFileName, calName, orgLabels, \
        orgStatusFuture, orgStatusCurrent, orgStatusPast, orgStatusCancel, \
        orgPrioDefault, orgPrioHigh, orgPrioLow = readConfigFile()

# Setup an account:
account = setupAccount(username,password, server, emailAddress)



# Start and end date to fetch calendar items for:
now       = account.default_timezone.localize(EWSDateTime.now())
startDate = now - timedelta(days=daysPast)
endDate   = now + timedelta(days=daysFuture)
# startDate = account.default_timezone.localize(EWSDateTime(2019, 11, 7))
# endDate   = account.default_timezone.localize(EWSDateTime(2019, 11, 8))


# Desired timezone:
if timezone=='':
    tz = EWSTimeZone.localzone()
else:
    tz = EWSTimeZone.timezone(timezone)


# # Line-ending replacement strings:
# # https://stackoverflow.com/a/43678795/1386750
WINDOWS_LINE_ENDING = str('\r\n')
UNIX_LINE_ENDING = str('\n')


# Open output file and write header line with calendar name and orgmode labels:
outFile = open(outFileName, 'w')
outFile.write('* '+calName+'  '+orgLabels+'\n')

INDENT=''
items = account.calendar.view(start=startDate, end=endDate, max_items=maxItems)
for item in items:
    item_start = EWSDateTime.astimezone(item.start, tz)  # Start time of item in the desired timezone
    item_end   = EWSDateTime.astimezone(item.end,   tz)  # End time of item in the desired timezone
    
    # Set item status (e.g., TODO/DONE/CANCELLED):
    status = orgStatusFuture
    if(now > item_start):
        status = orgStatusCurrent
        if(now > item_end): status = orgStatusPast
    if(item.is_cancelled): status = orgStatusCancel
    if(status != ''): status += ' '
    
    prio = orgPrioDefault
    if(item.importance == 'High'):
        prio = orgPrioHigh
    elif(item.importance == 'Low'):
        prio = orgPrioLow
    if(prio != ''): prio += ' '
    
    # print(item_start.date(), item_start.time(), item_end.time(), item.subject, item.location, status, prio, item.importance)
        
    outFile.write('\n** '+status+prio+item.subject+'\n')
    outFile.write(INDENT+item_start.strftime('<%Y-%m-%d %a %H:%M-')+item_end.strftime('%H:%M>\n'))
    
    # Body:
    if(item.text_body != None):
        content = str(item.text_body.strip()+'\n')
        #print(type(content))
        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        outFile.write(content)
        #outFile.write(htmlstrip.strip_tags(content))
    elif(item.body != None):
        #outFile.write(item.body.strip()+'\n')
        content = str(item.body.strip()+'\n')
        # print("Content: "+content )
        # print(type(content))
        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        #outFile.write(content)
        outFile.write(htmlstrip.strip_tags(content))

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
    #if(item.location != None):
    outFile.write(INDENT+':LOCATION:   '+str(item.location)+'\n')
    
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
        outFile.write(INDENT+':CREATED:    '+item.datetime_created.strftime('[%Y-%m-%d %a %H:%M] \n'))
        
    if(item.web_client_read_form_query_string != None):
        outFile.write(INDENT+':LINK:       [['+item.web_client_read_form_query_string+'][Outlook]] \n')
        
    if(item.web_client_edit_form_query_string != None):
        outFile.write(INDENT+':LINK:       [['+item.web_client_edit_form_query_string+'][Outlook edit]] \n')
    
    # if(item.XXX != None):
    #     outFile.write(INDENT+':XXX: '+str(item.XXX)+'\n')
    
    outFile.write(INDENT+':END:\n')
    
outFile.close()
    
