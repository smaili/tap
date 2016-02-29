# -*- coding: utf-8 -*-
#------------------------------------------------------------------------
#
#     /$$      /$$                           /$$
#    | $$  /$ | $$                          | $$
#    | $$ /$$$| $$  /$$$$$$   /$$$$$$   /$$$$$$$
#    | $$/$$ $$ $$ /$$__  $$ /$$__  $$ /$$__  $$
#    | $$$$_  $$$$| $$$$$$$$| $$$$$$$$| $$  | $$
#    | $$$/ \  $$$| $$_____/| $$_____/| $$  | $$
#    | $$/   \  $$|  $$$$$$$|  $$$$$$$|  $$$$$$$
#    |__/     \__/ \_______/ \_______/ \_______/
#     weed.py
#     This is the main python file for determining
#     direct download links for the video website
#     videoweed.es.
#
#------------------------------------------------------------------------


# Imports
#------------------------------------------------------------------------
import re, sys, urllib2, time

sys.dont_write_bytecode = True


# Constants
#------------------------------------------------------------------------
TIMEOUT = 10 # 10 seconds
SLEEP_WAIT = 1 # 1 second
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'


# Functions
#------------------------------------------------------------------------
def _get( url ):
    while True:
        try:
            req = urllib2.Request( url, headers={ 'User-Agent': UA } )
            return urllib2.urlopen( req , timeout=TIMEOUT ).read()
        except:
            time.sleep( SLEEP_WAIT )


def get_media_url( web_url ):
    #grab stream details
    html = _get( web_url )

    r = re.search( 'flashvars.domain="(.+?)".*flashvars.file="(.+?)".*' + 
                   'flashvars.filekey="(.+?)"', html, re.DOTALL )

    #use api to find stream address
    if r:
        domain, fileid, filekey = r.groups()
        api_call = ( '%s/api/player.api.php?user=undefined&codes=1&file=%s' +
                    '&pass=undefined&key=%s') % ( domain, fileid, filekey )

    api_html = _get( api_call )
    rapi = re.search( 'url=(.+?)&title=', api_html )

    if rapi:
        stream_url = rapi.group( 1 )

    return stream_url


# Main
#------------------------------------------------------------------------
if __name__=="__main__":
    try:
        args = sys.argv
        for i in range( 1, len( args ) ):
            url = args[ i ]
            url = get_media_url( url )
            print url

    except Exception, e:
        print e
        print ""
        print "To use: python weed.py weed_url_1 weed_url_2 ... weed_url_n"
        print ""