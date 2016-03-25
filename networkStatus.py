#!/usr/bin/python2

"""Shows the current network status for all nodes in the directory consensus"""

import sys
import socket
from stem.control import Controller

def main():
	with Controller.from_port(port = 9051) as controller:
		controller.authenticate("")
		for desc in controller.get_network_statuses():
			print desc.nickname,"=>",desc.address,", PUBLISHED=",desc.published,", BANDWIDTH=",desc.bandwidth

if __name__ == "__main__":
	sys.exit(main())
			
