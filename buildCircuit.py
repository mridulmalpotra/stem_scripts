#!/usr/bin/python2

"""
Tool for custom circuit creation. 
If OR nickname or hash mentioned, the information is accordingly used.
Otherwise, random selection of 3 ORs out of the cached network consensus is used.
"""

import stem.control
import sys
import random


routers = []


def routers_rand():
    global routers
    consensus = []
    for i in controller.get_network_statuses():
        consensus+=[i]
    for i in xrange(3):
        routers += [str(consensus[random.randint(0,len(consensus)-1)].nickname)]
    return


def main():
    with stem.control.Controller.from_port(port=9051) as controller:
        controller.authenticate("") # Change according to authentication measures
        routers = []
        if sys.argv[1] == 'rand':
            routers_rand()
            sys.argv[1] = 0
        else:
            if len(sys.argv) < 3:
                print "Specify at least one OR"
                sys.exit(1)
            else:
                routers = sys.argv[2:]
                for i in xrange(len(routers)):
                    routers[i] = "IIITD"+routers[i]
        print 'Routers =>',routers
        circuit_id = controller.extend_circuit(sys.argv[1], routers)
        if sys.argv[1] == '0':
            print "Circuit created with circuit ID: ", circuit_id
        else:
            print "Circuit extended with circuit ID: ", circuit_id
    return


if __name__ == "__main__":
    sys.exit(main())