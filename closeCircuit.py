#!/usr/bin/python2

"""
Tool for custom circuit deletion. 
If OR nickname or hash mentioned, the information is accordingly used.
If 'all' is mentioned, all circuits are removed.
"""

import sys
from stem import CircStatus
from stem.control import Controller


def main():
    if len(sys.argv) < 2:
        print "No valid circuit ID provided"

    else:
        with Controller.from_port(port = 9051) as controller:
            controller.authenticate("") # Change according to authentication measures
            if (sys.argv[1] is 'all'):
                for circ in sorted(controller.get_circuits()):
                    if circ.status != CircStatus.BUILT:
                        continue
                    else:
                        controller.close_circuit(circ.id)
            else:
                for circ in sys.argv[1:]:
                    controller.close_circuit(circ)


if __name__ == "__main__":
    sys.exit(main())
