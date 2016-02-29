# -*- coding: utf-8 -*-
#------------------------------------------------------------------------
#
#     /$$$$$$$$
#    |__  $$__/
#       | $$  /$$$$$$   /$$$$$$
#       | $$ |____  $$ /$$__  $$
#       | $$  /$$$$$$$| $$  \ $$
#       | $$ /$$__  $$| $$  | $$
#       | $$|  $$$$$$$| $$$$$$$/
#       |__/ \_______/| $$____/
#                     | $$
#                     | $$
#                     |__/
#     tap.py
#     This is the main python file for continuously checking a url
#     until the desired search string is found.
#
#------------------------------------------------------------------------


# Imports
#------------------------------------------------------------------------
import sys, urllib2, time

sys.dont_write_bytecode = True


# Constants
#------------------------------------------------------------------------
TIMEOUT = 20 # 20 seconds
SLEEP_WAIT = 120 # 2 minutes
NEEDLE = '' # text to search for
URL = '' # url to tap
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36' # user agent to use


# Functions
#------------------------------------------------------------------------
def beep():
    sys.stdout.write( '\a' )
    sys.stdout.flush()


def alert():
    while True:
        # beep 5 times
        for i in range( 0, 5 ):
            beep()
        time.sleep( 3 ) # wait 3 seconds


def _get( url ):
    while True:
        try:
            req = urllib2.Request( url, headers={ 'User-Agent': UA } )
            return urllib2.urlopen( req , timeout=TIMEOUT ).read()
        except:
            time.sleep( SLEEP_WAIT )


def check( url ):
    html = _get(url)
    if html:
        if NEEDLE in html:
            alert()

    return False


def go():
    print ""
    print "Checking site"
    print ""

    while True:
        url = URL
        result = check( url )
        if result:
            break
        time.sleep( SLEEP_WAIT )

    print "Content found"
    print ""


# Main
#------------------------------------------------------------------------
if __name__=="__main__":
    try:
        go()

    except:
        print ""
        print "To use: python nfl.py"
        print ""