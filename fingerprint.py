import os
import sys
import urllib2
from optparse import OptionParser

parser = OptionParser(usage="usage: sudo %prog [options]")
parser.add_option("-t", "--target", action="store", dest="target", type=str, help="Server to fingerprint")
(options, args) = parser.parse_args()

#handle colors
OK_GREEN = "\033[92m"
OK_BLUE = "\033[94m"
ERR = "\033[91m"
ENDC = "\033[0m"

def printMsg(s):
    print(OK_BLUE + "[*]" + ENDC + " " + s)
def printGood(s):
    print(OK_GREEN + "[*]" + ENDC + " " + s)
def printErr(s):
    print(ERR + "[!]" + ENDC + " " + s)


if len(args) == 1:
    printErr("Missing the required \'-t\' option")
    printErr("Exiting...")
    exit(1)
else:
    try:
        request = urllib2.Request(options.target)
        request.add_header('User-Agent', 'curl/7.37.0')
        response = urllib2.urlopen(request)
        printGood("Results brought back server type of: " + OK_GREEN + response.info().getheader('Server') + ENDC)
        exit(0)
    except (ValueError, urllib2.URLError) as e:
        printErr("Server didn't respond. Exiting...")
        exit(1)
