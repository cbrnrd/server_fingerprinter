# Server Fingerprinter

#### Usage:

```
Usage: python fingerprint.py -t example.com [options]

Options:
  -h, --help            show this help message and exit
  -t, --target          Target web server to fingerprint
  -n, --nmap            Performs a full nmap scan on the target (Requires nmap)
  -s, --search          Searches exploit-db for the returned server type
  --sub                 Prepends a subdomain to the value of '-t'. Default: www
  -u UAGENT, --user-agent=UAGENT: The fake(or real) user agent to use. (defaults to "curl/7.37.0")
```
