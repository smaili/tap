# -*- coding: utf-8 -*-
#------------------------------------------------------------------------
#
#     /$$      /$$                           /$$  /$$$$$$  /$$ /$$                    
#    | $$  /$ | $$                          | $$ /$$__  $$| $$| $$                    
#    | $$ /$$$| $$  /$$$$$$   /$$$$$$   /$$$$$$$| $$  \ $$| $$| $$ /$$   /$$  /$$$$$$$
#    | $$/$$ $$ $$ /$$__  $$ /$$__  $$ /$$__  $$| $$$$$$$$| $$| $$| $$  | $$ /$$_____/
#    | $$$$_  $$$$| $$$$$$$$| $$$$$$$$| $$  | $$| $$__  $$| $$| $$| $$  | $$| $$      
#    | $$$/ \  $$$| $$_____/| $$_____/| $$  | $$| $$  | $$| $$| $$| $$  | $$| $$      
#    | $$/   \  $$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$  | $$| $$| $$|  $$$$$$/|  $$$$$$$
#    |__/     \__/ \_______/ \_______/ \_______/|__/  |__/|__/|__/ \______/  \_______/
#     weedalluc.py
#     This is the main python file for listing the
#     direct download links for the video website
#     videoweed.es by batch searching alluc.com.
#
#------------------------------------------------------------------------


# Imports
#------------------------------------------------------------------------
import re, sys, urllib2, time

sys.dont_write_bytecode = True


# Constants
#------------------------------------------------------------------------
ALLUC_SEARCH_FORMAT = 'http://www.alluc.com/stream/dragonballz-%s.flv+host%%3Avideoweed.es'
ALLUC_SEARCH_REGEX = '<div class=title><a href="(.+?)" target=_blank>dragonballz-%s.flv</a></div>'


TIMEOUT = 10 # 10 seconds
SLEEP_WAIT = 1 # 1 second
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
ACCEPT_LANGUAGE = 'en-US,en;q=0.8'
COOKIE = 'nlbi_265955=1UP1fBzMcFf1hs82p6CPvAAAAACYUdi2CXMIu/gf0bdwQefJ; incap_ses_197_265955=MSvde1V2whY4h0xD9+K7AiDtJFUAAAAAFlGun9j878mJYKqLEXZLgw==; LG=CN; incap_ses_259_265955=CxpxZb85zS2gxjHImSeYAyDtJFUAAAAA1rrSRfduS1z6j5v6/yMuZw==; _gat=1; incap_ses_47_265955=fGGYBkdwFxfwU/8wMPymAKauKVUAAAAAK5zlNNXp0dNrbr5cgFsw5A==; visid_incap_265955=Qq5bmX/DSRGVx4557UNr/iAhElUAAAAAQUIPAAAAAAD2ccmGTSGZ5xVgiq+/eW2r; incap_ses_108_265955=QZ1QSPB+OgO+lnC92LJ/AZ6uKVUAAAAAqBq8iZe3aqWuSJXhnAQ6iA==; lastSearch=[{"word":"scorpion","timestamp":1427251494},{"word":"scorpion.118.hdtv-lol.mp4","timestamp":1427251529},{"word":"the.flash.2014.115.hdtv-lol.mp4","timestamp":1427424044},{"word":"dragonballz-151.flv host:videoweed.es","timestamp":1427424119},{"word":"dragonballz-153.flv host:videoweed.es","timestamp":1427433115},{"word":"girl.meets","timestamp":1427796769},{"word":"girl.meets.world","timestamp":1427796790},{"word":"the.big.bang","timestamp":1428483373},{"word":"dragonballz-251.flv host:videoweed.es","timestamp":1428795039},{"word":"dragonballz-262.flv host:videoweed.es","timestamp":1428795545}]; _ga=GA1.2.1588426621.1427251494; __atuvc=7%7C12%2C6%7C13%2C4%7C14%2C3%7C15; __atuvs=5529ae9fea8c7506002'


# Functions
#------------------------------------------------------------------------
def _get( url ):
    while True:
        try:
            req = urllib2.Request( url, headers={ 'User-Agent': UA, 'Accept': ACCEPT, 'Accept-Language': ACCEPT_LANGUAGE, 'Cookie': COOKIE } )
            return urllib2.urlopen( req , timeout=TIMEOUT ).read()
        except:
            time.sleep( SLEEP_WAIT )


def get_media_url( number ):
    # to string
    strnum = str( number )

    # prepend necessary zeros to ensure three digits
    if number < 10:
        strnum = '0' + strnum
    if number < 100:
        strnum = '0' + strnum

    # form search url
    search_url = ALLUC_SEARCH_FORMAT % strnum

    print '%s %s' % ( strnum, search_url )

    #grab search details
    html = _get( search_url )

    # regex
    r = re.search( ALLUC_SEARCH_REGEX % strnum, html, re.DOTALL )

    # follow link
    if r:
        link = r.groups()
        item_url = ( 'http://www.alluc.com%s') % ( link )

        html = _get( item_url )

        r = re.search( '<textarea onClick="this.select\(\);">(.+?)\n</textarea>', html )

        if r:
            media_url = r.group( 1 )

            return media_url
    else:
        r = re.search( 'No results.\nTry', html )

        if r:
            return 'NO RESULTS FOR %s' % strnum

    # not found, try again...
    return get_media_url( number )


# Main
#------------------------------------------------------------------------
if __name__=="__main__":
    try:
        args = sys.argv
        start = int( args[ 1 ] )
        end = int( args[ 2 ] )
        urls = ''
        for i in range( start, end + 1 ):
            url = get_media_url( i )
            urls = urls + url + ' '

        print urls

    except Exception, e:
        print e
        print ""
        print "To use: python weedalluc.py startN endN"
        print ""