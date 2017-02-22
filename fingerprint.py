#!/usr/bin/python
import urllib2
import sys
import socket
import threading
import requests
from time import sleep
from subprocess import call
from optparse import OptionParser

parser = OptionParser(usage="Usage: python fingerprint.py -t target [-u User-Agent]\nProper url format: example.com (no http or www)")
parser.add_option("-t", "--target", action="store", dest="target", type=str, help="Server to fingerprint")
parser.add_option("-u", "--user-agent", action="store", dest="uagent", type=str, default="curl/7.37.0", help="The fake(or real) user agent to use. (defaults to \"curl/7.37.0\")")
parser.add_option("-n", "--nmap", action="store_true", dest="nmapScan", default=False, help="Perform an nmap OS scan on the target. (Requires nmap in $PATH)")
parser.add_option("-s", "--search", action="store_true", dest="searchsploit", default=False, help="use searchsploit to search exploit-db for exploits (Requires searchsploit in $PATH)")
parser.add_option("--sub", action="store_true", dest="subdomain", default="www", help="Prepends a subdomain to the value of domain")
parser.add_option("-x", "--x-powered", action="store_true", dest="xpowered", default=False, help="Gets `x-powered by' header, if there is one.")
parser.add_option("--ssl", action="store_true", dest="ssl", default=False, help="Uses https instead of http (Default: False)")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Use verbose output")
parser.add_option("--raw", action="store_true", dest="raw_url", default=False, help="Use the exact input of -t as url")
parser.add_option("--scan", action="store_true", dest="scan", default=False, help="Do a basic portscan of target if no server is found")
(options, args) = parser.parse_args()


if len(sys.argv) == 1:
	print "\n"
	parser.print_help()
	exit(1)

if options.raw_url:
	url = str(options.target)
	
elif not options.ssl:
	url = "http://" + options.subdomain + "." + str(options.target)

else:
	url = "https://" + options.subdomain + "." + str(options.target)

def sleep(i):
	time.sleep(i)

# handle colors
OK_GREEN = "\033[92m"
OK_BLUE = "\033[94m"
ERR = "\033[91m"
ENDC = "\033[0m"


def print_msg(s):
    print(OK_BLUE + "[*]" + ENDC + " " + s)


def print_good(s):
    print(OK_GREEN + "[+]" + ENDC + " " + s)


def print_err(s):
    print(ERR + "[!]" + ENDC + " " + s)


def portscan(tgt, prt):
	tgtip = tgt.gethostbyname(tgt)
	try:
		for i in range(1, int(prt)):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((tgtip, int(prt))
			if result is 0:
				print "Port: {} is open".format(i)
				if i == 22:
					print_msg("Port 22 is open, trying to fingerprint (OS and ssh server)...")
					req = requests.get(tgt + ":22")
					res = req.text
					if not res:
						print_err("{} returned nothing on port 22".format(tgtip)
					else:
						print_good("%s returned %s on port 22" % tgtip, res)
					
			sock.close()
	except socket.gaierror:
		print_err('Hostname could not be resolved. Exiting')
		sys.exit()
	
# make '-t' a required argument
if not options.target:
    print_err("Missing the required \'-t\' option")
    print_err("Exiting...")
else:
    try:
        print_msg("Trying to contact %s..." % url)
        request = urllib2.Request(url)
        request.add_header('User-Agent', options.uagent)
        response = urllib2.urlopen(request)
        try:
            serverType = response.info().getheader('Server')
            print_good("Results brought back server type of: " + OK_GREEN + serverType + ENDC) # parse 'Server:' header in response packet
            if options.xpowered: # handle -x flag
                if options.verbose:
                    print_msg("Performing x-ray... (get it?)")
                try:
                    xpwered = response.info().getheader('X-Powered-By')
                    if options.verbose:
                        print_msg("We got a hit!")
                    print_good(url + "is X-Powered-By: " + "\033[93m" + xpwered + "\033[0m")
                except TypeError as typer:
                    print_err("Server didn't send back an `X-Powered-By' header. Good for them.")
            if options.nmapScan: # handle -n flag
                print "\n"
		print_msg("Starting nmap scan, hold on...") #idek why i have to indent this line like this. DO NOT TOUCH THIS YOU WILL SCREW IT UP
                call(["sudo", "nmap", "-O", "-sV", "-v", options.target]) # nmap scan command
            if options.searchsploit: # handle -s flag
                try:
                    print_msg("Searching exploit-db.com for " + serverType + "...")
                    call(["searchsploit", serverType])
                except OSError as oserr:
                    print_err("Searchsploit couldn't be found in the system path.")
        except TypeError as typeerr: # if there is no response header
            print_err("Server responded with no server header.")
	    	if scan:
				print_msg("Doing port scan on {} (tcp/1-1024)".format(target))
				portscan(target, port)
				
        print_err("Exiting...")
        exit(0)
    except urllib2.URLError as urlerr:  # if the server didn't respond
        print_err("Server didn't respond. (check the URL)")
        print_err("Exiting...")
        exit(1)
    except ValueError as valerr:  # if the url is a bad url

	if options.raw_url:
		print_err("Use a service in your url (http:// ftp:// etc.)")
		print_err("Exiting")
		exit(1)
	else:
        	print_err("Please put in a valid url. (WITHOUT http:// and www.)")
        	print_err("Exiting... ")
        	exit(1)
