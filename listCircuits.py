#!/usr/bin/python2

"""
Tool for custom circuit listing. 
If OR nickname or hash mentioned, the information is accordingly used.
Otherwise, random selection of 3 ORs out of the cached network consensus is used.
"""

def main():
    from stem import CircStatus
    from stem.control import Controller

    with Controller.from_port(port = 9051) as controller:
        controller.authenticate("")
        for circ in sorted(controller.get_circuits()):
            print ""

            # Can be changed for different levels of circuit-creation.
            if circ.status != CircStatus.BUILT:
                print "Not yet built!!"

            print "Circuit",circ.id,"(",circ.purpose,")")

            for i, entry in enumerate(circ.path):
                div = '+' if (i == len(circ.path) - 1) else '|'
                fingerprint, nickname = entry

                desc = controller.get_network_status(fingerprint, None)
                address = desc.address if desc else 'unknown'

                print(" %s- %s (%s, %s)" % (div, fingerprint, nickname, address))


if __name__ == "__main__":
    sys.exit(main())