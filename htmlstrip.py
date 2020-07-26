#!/usr/bin/python3
# MLStripper stolen from https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
# and some from https://stackoverflow.com/questions/3075550/how-can-i-get-href-links-from-html-using-python
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    ##self.links = chain(self.links, [value])
                    self.text.write(value)

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()

    def handle_comment(self, data):
        print("Comment  :", data)
    
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# htmlString = '''<html>
# <head>
# <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
# <meta name=\"Generator\" content=\"Microsoft Exchange Server\">
# <!-- converted from rtf -->
# <style><!-- .EmailQuote { margin-left: 1pt; padding-left: 4pt; border-left: #800000 2px solid; } --></style>
# </head>
# <body>
# <font face=\"Times New Roman\" size=\"3\"><span style=\"font-size:12pt;\"><a name=\"BM_BEGIN\"></a>
# <div><br>
# 
# &nbsp; ________________________________&nbsp;&nbsp; Nuo: Arvydas LaurinavičiusVarduVpcMokslas Išsiųsta: 2020 m. birželio 4 d., ketvirtadienis 22:14:07 (UTC&#43;02:00) Helsinkis, Kijevas, Ryga, Sofija, Talinas, Vilnius Iki: Arvydas Laurinavičius Kopija: Erinija Pranckevičienė;
# Benoît PLANCOULAINE; Renaldas Augulis; Dovilė Žilėnaitė; Aistė Vitkūnaitė; Aida.Laurinaviciene; Ernesta.Vieraityte (Guest) Tema: DeepAnythingTeams Kada: Vyksta kas antradienis nuo 08:30 iki 10:00 galioja 2020-04-07. FLE Standard Time Kur:
# <br>
# 
# Adding new members. </div>
# <div><font color=\"gray\">________________________________________________________________________________</font></div>
# <div><a href=\"https://teams.microsoft.com/l/meetup-join/19%3aafe706147c8b4ad6959c8a4fe58d5ee6%40thread.tacv2/1585822644365?context=%7b%22Tid%22%3a%2282c51a82-548d-43ca-bcf9-bf4b7eb1d012%22%2c%22Oid%22%3a%225b77d2ea-8044-4243-b01d-5bf8c9d86c5b%22%7d\"><font face=\"Segoe UI Semibold\" size=\"2\" color=\"#6264A7\"><span style=\"font-size:10.5pt;\"><u>Join
# Microsoft Teams Meeting</u></span></font></a></div>
# <div style=\"margin-top:6pt;\"><a href=\"https://aka.ms/JoinTeamsMeeting\"><font face=\"Segoe UI\" size=\"1\" color=\"#6264A7\"><span style=\"font-size:7pt;\">Learn more about Teams</span></font></a><font face=\"Segoe UI\" color=\"#252424\"> | </font><a href=\"https://teams.microsoft.com/meetingOptions/?organizerId=5b77d2ea-8044-4243-b01d-5bf8c9d86c5b&amp;tenantId=82c51a82-548d-43ca-bcf9-bf4b7eb1d012&amp;threadId=19_afe706147c8b4ad6959c8a4fe58d5ee6@thread.tacv2&amp;messageId=1585822644365&amp;language=en-US\"><font face=\"Segoe UI\" size=\"1\" color=\"#6264A7\"><span style=\"font-size:7pt;\">Meeting
# options</span></font></a><font face=\"Segoe UI\" color=\"#252424\"> </font></div>
# <div>&nbsp;</div>
# <div style=\"margin-top:2.4pt;\">&nbsp;</div>
# <div><font color=\"gray\">________________________________________________________________________________</font></div>
# </span></font>
# </body>
# </html>'''

# ##print(htmlString)

# print(strip_tags(htmlString))
