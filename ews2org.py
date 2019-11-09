#!/bin/env python3

# https://pypi.org/project/exchangelib/

# https://stackoverflow.com/a/46649097/1386750
from exchangelib import DELEGATE, Account, Credentials, Configuration, EWSDateTime, EWSTimeZone

creds = Credentials(
    username="xxx@xxx.nn", 
    password="xxx"
)

config = Configuration(server='server.address.org', credentials=creds)

account = Account(
    primary_smtp_address="xxx@xxx.nn",
    autodiscover=False, 
    config=config,
    access_type=DELEGATE
)


start = account.default_timezone.localize(EWSDateTime(2019, 11, 7))
end = account.default_timezone.localize(EWSDateTime(2019, 11, 8))

tz = EWSTimeZone.localzone()



INDENT='    '
items = account.calendar.view(start=start, end=end)
for item in items:
    item_start = EWSDateTime.astimezone(item.start,tz)
    item_end = EWSDateTime.astimezone(item.end,tz)
    #print(item_start.date(), item_start.time(), item_end.time(), item.subject, item.location)
    
    print('\n**',item.subject)
    print(INDENT+'SCHEDULED '+item_start.strftime('<%Y-%m-%d %a %H:%M-')+item_end.strftime('%H:%M>'))
    if(item.text_body != None):
        print(item.text_body.strip())
    elif(item.body != None):
        print(item.body.strip())
    
    print(INDENT+':PROPERTIES:')
    
    # People:
    if(item.organizer != None):
        print(INDENT+':ORGANISER:  ', item.organizer.name+' <'+item.organizer.email_address+'>')
        
    if(item.required_attendees != None):
        #print(INDENT+':ATTENDEES:  ', item.required_attendees)
        print(INDENT+':ATTENDEES:  ')
        for att in item.required_attendees:
            print(INDENT+'  :ATTENDEE:   '+att.mailbox.name+' ('+att.response_type+')')
            
    
    if(item.optional_attendees != None):
        #print(INDENT+':ATTENDEES:  ', item.optional_attendees)
        print(INDENT+':ATTENDEES:  ')
        for att in item.optional_attendees:
            print(INDENT+'  :ATTENDEE:   '+att.mailbox.name+' ('+att.response_type+')')
            
    
    # Metadata:
    if(item.my_response_type != None):
        print(INDENT+':RESPONSE:   ', item.my_response_type)
    
    if(item.importance != None):
        print(INDENT+':PRIORITY:   ', item.importance)
        
    if(item.is_cancelled != None):
        print(INDENT+':CANCELLED:  ', item.is_cancelled)
        
    if(item.categories != None):
        #print(INDENT+':CATEGORIES: ', item.categories)
        print(INDENT+':CATEGORIES:  ', end=' ')
        for cat in item.categories:
            print(cat, end=' ')
        print()
        
    if(item.conflicting_meeting_count != None):
        print(INDENT+':CONFLICTS:  ', item.conflicting_meeting_count)
        
    if(item.adjacent_meeting_count != None):
        print(INDENT+':ADJACENT:   ', item.adjacent_meeting_count)
        
    if(item.is_recurring != None):
        print(INDENT+':RECURRING:  ', item.is_recurring)
        
        if(item.recurrence != None):
            print(INDENT+'  :RECURRENCE: ', item.recurrence)
        
        if(item.first_occurrence != None):
            print(INDENT+':FIRST OCCURRENCE: ', item.first_occurrence)
        
        if(item.last_occurrence != None):
            print(INDENT+':LAST OCCURRENCE: ', item.last_occurrence)

    
    if(item.headers != None):
        print(INDENT+':HEADERS:    '+item.headers)
        
    if(item.datetime_created != None):
        print(INDENT+':CREATED:     '+item.datetime_created.strftime('[%Y-%m-%d %a %H:%M]'))
        
    if(item.web_client_read_form_query_string != None):
        print(INDENT+':LINK:        [['+item.web_client_read_form_query_string+'][Outlook]]')
        
    if(item.web_client_edit_form_query_string != None):
        print(INDENT+':LINK:        [['+item.web_client_edit_form_query_string+'][Outlook edit]]')
    
    # if(item.XXX != None):
    #     print(INDENT+':XXX: ', item.XXX)
    
    print(INDENT+':END:')
    
    
