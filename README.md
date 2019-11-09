# ews2org: download an EWS/Exchange/Outlook/Office365 calendar and convert it to emacs orgmode #

This repo currently consists of a single, simple Python script, `ews2orgCal.py`, which downloads selected (in
time) calendar items from a Micro$oft EWS server and saves them in emacs orgmode format.  All the work is
really done by [exchangelib](https://github.com/ecederstrand/exchangelib).  I run the script in a cron job to
sync my work calendar one-way.


## Installation, configuration and use ##

1. `pip install exchangelib`
2. Download this script and the example config file, rename the latter to ews2org.cfg and edit it to match
   your server and account.
3. Run ews2orgCal.py in the directory where ews2org.cfg is located and give it a few seconds.


## Notes ##

Originally, my script ran on the command line, but not as a cron job.  I got an error like
`UnicodeEncodeError: 'latin-1' codec can't encode characters in position 393-401: ordinal not in range(256)`.
I had to make sure I used UTF8 in cron, by adding `LANG="en_US.utf8"` (instead of my `LANG="en_US"` to the
crontab.

