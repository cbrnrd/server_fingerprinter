import os
import sys
import urllib2
from optparse import OptionParser

parser = OptionParser(usage="usage: sudo %prog [options]")
parser.add_option("-t", "--target", action="store", dest="target", type=str, help="Server to fingerprint")
parser.add_option("-u", "--user-agent", action="store", dest="uagent", type=str, default="curl/7.37.0", help="The fake(or real) user agent to use. (defaults to \"curl/7.37.0\"")
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


if not options.target:
    printErr("Missing the required \'-t\' option")
    printErr("Exiting...")
else:
    try:
        printMsg("Trying to contact %s..." % options.target)
        request = urllib2.Request(options.target)
        request.add_header('User-Agent', options.uagent)
        response = urllib2.urlopen(request)
        try:
            printGood("Results brought back server type of: " + OK_GREEN + response.info().getheader('Server') + ENDC)
        except TypeError as typeerr:
            printErr("Server responded with no server type or a spoofed server type.")
            printErr("Exiting...")
        exit(0)
    except urllib2.URLError as urlerr:
        printErr("Server didn't respond. (check the URL)")
        printErr("Exiting...")
        exit(1)
    except ValueError as valerr:
        printErr("Please put in a valid url. (with https:// and www.)")
        printErr("Exiting... ")
        exit(1)
