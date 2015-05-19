import commands

DEBUG = True
KODI_URI = 'http://localhost:8080'

if DEBUG:
    # If we are connected to BLUEZONE, assume that we wish to use our local Kodi installation
    output = commands.getstatusoutput('nmcli con status')
    if 'BLUEZONE' in output[1]:
        KODI_URI = 'http://localhost:8080'
