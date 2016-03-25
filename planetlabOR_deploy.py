#!/usr/bin/python2

"""
Tor deployment on PlanetLab
- install Tor and other respective dependencies
- remove conflicting packages
- uses older Tor version to support Fedora 8 machines on PlanetLab
"""

import subprocess
import urllib2
import sys


output = ""
err = ""


def execute(string):
    """
    Execute a command using the subprocess module and Popen

    :param string: str
    """
    global output, err
    p = subprocess.Popen(string, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = output.lower()
    if err is not None:
        err = err.lower()
    return


def create_dirs():
    """ Initializes a new tor data directory"""
    global output, err
    try:
        execute("rm -rf ~/tor && mkdir ~/tor && mkdir ~/tor/keys")
        print "Created directories"
    except Exception, e:
        print e.message
        print "Exception, returning!"
        return


def generate_torrc():
    """ Removes old torrc files in home directory, adds new file and appends Onion router ID"""
    global output, err
    try:
        # Set up a globally accessible torrc file for all onion routers
        execute("cd && rm -f ~/torrc* && wget <Publically hosted torrc file URL>"
                "~/torrc")
        print "output is =>", output
        
        # Mention the ID assigning server that gives a unique number that can be added to the OR,
        # thereby making it have a unique username.
        
        response = urllib2.urlopen("""<Insert Socket for ID assigning server>""")
        num = response.read()
        print "num is =>", num
        if len(num) > 0:
            execute("echo Nickname IIITDOR"+num+" >> ~/torrc")
        else:
            print "ID not found. Continuing..."
    except Exception, e:
        print e.message
        print "Exception, returing!"
        return


def start_tor():
    """ Start tor with torrc and kill any previous instances"""
    global output, err
    try:
        execute("killall tor")
        execute("/usr/local/bin/tor -f ~/torrc")
    except Exception, e:
        print e.message
        print "Exception, returing!"
        return


def install_dependencies():
    """ Removes pre-installed tor. Installs gcc, vim, libevent-devel and openssl-devel"""
    global output, err
    try:
        execute("sudo yum remove tor -y")
        print output
        execute("sudo yum install gcc vim make libevent-devel openssl-devel --nogpgcheck -y")
        print output
        if "nothing to do" not in output and "complete" not in output:
            assert True
    except Exception, e:
        print e.message
        print "Exception, returing!"
        return


def install_tor():
    """ Downloads tor source and compiles using standard autoconf steps"""
    global output, err
    try:
        execute("cd && rm -f tor_source.tar.gz && wget https://launchpad.net/ubuntu/+archive/primary/+files/"
                    "tor_0.2.4.23.orig.tar.gz -O tor_source.tar.gz")
        print "output =>", output
        if "saved" not in output:
            assert True
        print "downloaded"

        execute("cd && tar xvzf tor_source.tar.gz && cd tor-0.2.4.23 && pwd")
        print "output =>", output
        if "tor-0.2.4.23" not in output:
            assert True
        print "untarred"

        execute("cd ~/tor-0.2.4.23 && ./configure")
        print "output =>", output
        if "config.status" not in output:
            assert True
        print "configured"

        execute("cd ~/tor-0.2.4.23 && make")
        print "output =>",output
        if "make  all-am" not in output:
            assert True
        print "made"

        execute("cd ~/tor-0.2.4.23 && sudo make install")
        print "output =>",output
        if "make[1]: leaving directory" not in output:
            assert True
        print "installed"
    except Exception, e:
        print e.message
        print "Exception, returning!"
        return

def main():
    create_dirs()
    print "Returned from creating directories."
    install_dependencies()
    print "Returned from installing dependencies."
    install_tor()
    print "Returned from installing tor."
    generate_torrc()
    print "Returned from generating torrc."
    start_tor()
    print "Returned from starting tor."

if __name__ == '__main__':
    sys.exit(main())
    