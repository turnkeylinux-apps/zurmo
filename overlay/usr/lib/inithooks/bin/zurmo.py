#!/usr/bin/python
"""Set Zurmo admin password and domain to serve

Option:
    --pass=     unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=www.example.com

"""

import sys
import getopt
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_DOMAIN="www.example.com"

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    domain = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Zurmo Password",
            "Enter new password for the Zurmo 'admin' account.")

    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "Zurmo Domain",
            "Enter the domain to serve Zurmo.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    '''
    hash = hashlib.md5(password).hexdigest()

    m = MySQL()
    m.execute('UPDATE zurmo._user SET hash=\"%s\" WHERE username=\"admin\";' % hash)
    '''
    
    zurmo = "/var/www/zurmo/app/protected/commands/"
    system("cd %s;./zurmoc changePassword --username=admin --password=%s" % (zurmo, password))

    conf = "/var/www/zurmo/app/protected/config/perInstance.php"
    system("sed -i \"s|hostInfo.*|hostInfo'] = 'http://%s';|\" %s" % (domain, conf))

if __name__ == "__main__":
    main()

