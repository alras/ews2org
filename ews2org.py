"""ews2org core functionality"""

from configparser import RawConfigParser
import os


def readConfigFile(debug=False):
    """Read the config file ews2org,cnf"""
    
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
        'orgmode_labels': ':Org:ews2cal:',  # Org mode labels
        
        'orgmode_status_future':  '',       # Default Org mode status future, e.g. TODO
        'orgmode_status_current': '',       # Default Org mode status current, e.g. PROGRESS
        'orgmode_status_past':    '',       # Default Org mode status past, e.g. DONE
        'orgmode_status_cancel':  '',       # Default Org mode status cancel, e.g. CANCELLED
        
        'orgmode_priority_default':  '',       # Default Org mode priority default, e.g. [#B] or empty
        'orgmode_priority_high':     '',       # Default Org mode priority high, e.g. [#A]
        'orgmode_priority_low':      '',       # Default Org mode priority low, e.g. [#C]
    })
    dir = os.path.dirname(os.path.realpath(__file__))
    config.read(os.path.join(dir, 'ews2org.cfg'))
    
    
    server        = config.get(   'ews2org',         'server')
    username      = config.get(   'ews2org',       'username')
    emailAddress  = config.get(   'ews2org',  'email_address')
    password      = config.get(   'ews2org',       'password')
    timezone      = config.get(   'ews2org',       'timezone')
    daysPast      = config.getint('ews2org',      'days_past')
    daysFuture    = config.getint('ews2org',    'days_future')
    maxItems      = config.getint('ews2org',      'max_items')
    outFileName   = config.get(   'ews2org',    'output_file')
    calName       = config.get(   'ews2org',  'calendar_name')
    orgLabels     = config.get(   'ews2org', 'orgmode_labels')
    
    orgStatusFuture   = config.get(   'ews2org', 'orgmode_status_future')
    orgStatusCurrent  = config.get(   'ews2org', 'orgmode_status_current')
    orgStatusPast     = config.get(   'ews2org', 'orgmode_status_past')
    orgStatusCancel   = config.get(   'ews2org', 'orgmode_status_cancel')
    
    orgPrioDefault   = config.get(   'ews2org', 'orgmode_priority_default')
    orgPrioHigh      = config.get(   'ews2org', 'orgmode_priority_high')
    orgPrioLow       = config.get(   'ews2org', 'orgmode_priority_low')
    
    
    # Check settings:
    if(debug):
        print("server:      ",        server)
        print("username:    ",      username)
        print("email:       ",  emailAddress)
        print("password:    ",      password)
        print("timezone:    ",      timezone)
        print()
        
        print("daysPast:    ",      daysPast)
        print("daysFuture:  ",    daysFuture)
        print("maxItems:    ",      maxItems)
        
        print()
        print("outFileName: ",   outFileName)
        print("calName:     ",       calName)
        print("orgLabels:   ",     orgLabels)
        print()
        
        print("orgStatusFuture:   ",     orgStatusFuture)
        print("orgStatusCurrent:  ",     orgStatusCurrent)
        print("orgStatusPast:     ",     orgStatusPast)
        print("orgStatusCancel:   ",     orgStatusCancel)
        print()
        
        print("orgPrioDefault:   ",     orgPrioDefault)
        print("orgPrioHigh:      ",     orgPrioHigh)
        print("orgPrioLow:       ",     orgPrioLow)
        print()
        
    
    return server, username, emailAddress, password, timezone, daysPast, daysFuture, \
        maxItems, outFileName, calName, orgLabels, \
        orgStatusFuture, orgStatusCurrent, orgStatusPast, orgStatusCancel, \
        orgPrioDefault, orgPrioHigh, orgPrioLow



def setupAccount(username,password, server, emailAddress):
    """Set up an account with an EWS server"""
    
    from exchangelib import DELEGATE, Account, Credentials, Configuration
    
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

    return account

