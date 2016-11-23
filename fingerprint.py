#!/usr/bin/python
import urllib2
from subprocess import call
from optparse import OptionParser

parser = OptionParser(usage="Usage: python fingerprint.py -t target [-u User-Agent]\nProper url format: example.com (no http or www)")
parser.add_option("-t", "--target", action="store", dest="target", type=str, help="Server to fingerprint")
parser.add_option("-u", "--user-agent", action="store", dest="uagent", type=str, default="curl/7.37.0", help="The fake(or real) user agent to use. (defaults to \"curl/7.37.0\")")
parser.add_option("-n", "--nmap", action="store_true", dest="nmapScan", default=False, help="Perform an nmap OS scan on the target.")
parser.add_option("-s", "--search", action="store_true", dest="searchsploit", default=False, help="use searchsploit to search exploit-db for exploits(Requires searchsploit)")
parser.add_option("--sub", action="store_true", dest="subdomain", default="www", help="Prepends a subdomain to the value of domain (Default www.)")
(options, args) = parser.parse_args()


url = "http://" + options.subdomain + "." + str(options.target)

# handle colors
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

# make '-t' a required argument
if not options.target:
    printErr("Missing the required \'-t\' option")
    printErr("Exiting...")
else:
    try:
        printMsg("Trying to contact %s..." % url)
        request = urllib2.Request(url)
        request.add_header('User-Agent', options.uagent)
        response = urllib2.urlopen(request)
        try:
            serverType = response.info().getheader('Server')
            printGood("Results brought back server type of: " + OK_GREEN + serverType + ENDC)

            printGood("Results brought back server type of: " + OK_GREEN + serverType + ENDC) # parse 'Server:' header in response packet
            if options.nmapScan == True:
                print "\n"
		printMsg("Starting nmap scan, hold on...") #idek why i have to indent this line like this
                call(["sudo", "nmap", "-O", "-sV", "-v", options.target]) # nmap scan command
            if options.searchsploit == True:
                try:
                    printMsg("Searching exploit-db.com for " + serverType + "...")
                    call(["searchsploit", serverType])
                except OSError as oserr:
                    printErr("Searchsploit couldn't be found in the system path.")
                    printErr("Exiting...")
        except TypeError as typeerr: # if there is no response header
            printErr("Server responded with no server header.")
            printErr("Exiting...")
        exit(0)
    except urllib2.URLError as urlerr:  # if the server didn't respond
        printErr("Server didn't respond. (check the URL)")
        printErr("Exiting...")
        exit(1)
    except ValueError as valerr:  # if the url is a bad url
        printErr("Please put in a valid url. (with http(s):// and www.)")
        printErr("Exiting... ")
        exit(1)
