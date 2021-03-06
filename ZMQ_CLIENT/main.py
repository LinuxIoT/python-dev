#!/usr/bin/python

__author__ = "Weqaar Janjua & Ahmer Malik"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "1.0"

import zmq
import sys
import signal
import threading
import ConfigParser
import socket
from time import *
from Database_queue import db_queue
from LITdb_writer import LIT_DB_Thread
import MySQLdb as sql
_thread_pool = []

class ZMQ_Client_HLL(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.queue = db_queue()
		

	def run(self):
		context = zmq.Context()
		print "Starting High-latency Service"
		socket = context.socket(zmq.PULL)
		socket.connect ("tcp://" + _meg_device_ip + ":%s" % _port_high_latency)
		print "Started, polling for messages (PULL) from: " + _meg_device_ip + "\n"
		poller = zmq.Poller()
		poller.register(socket, zmq.POLLIN)

        	while True:
			sleep(0.02)
			socks = dict(poller.poll())
        		if socket in socks and socks[socket] == zmq.POLLIN:
                		message = socket.recv()
				print message
			if message is None:
				pass
			else:
				self.queue.put(message)
				print "MESSAGE PUT: " + message + "\n"

class ZMQ_Client_LLL(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.queue = db_queue()

	def run(self):
		context = zmq.Context()
		print "Starting Low-latency Service"
		socket = context.socket(zmq.SUB)
		socket.setsockopt (zmq.SUBSCRIBE, '')
		socket.connect ("tcp://" + _meg_device_ip + ":%s" % _port_low_latency)
		print "Started, listening for messages (SUB) from: " + _meg_device_ip + "\n"

        	while True:
			sleep(0.02)
			message = socket.recv()
			print message
			if message is None:
				pass
			else:
				self.queue.put(message)
				print "MESSAGE PUT: " + message + "\n"


def main():
	_print_header()

	#global conf_file
	conf_file = "CZS.conf"

	#Initialize Config Parameters
	_conf = ConfigParser.ConfigParser()
	_conf.read(conf_file)

	#Read CZS Section
	_section = 'CZS'
	_high_latency = int(_conf.get(_section, 'high_latency'))
	_low_latency = int(_conf.get(_section, 'low_latency'))

	#Read ZMQ Section
	_section = 'ZMQ'
	global _port_high_latency
	global _port_low_latency
	global _meg_device_ip
	_port_high_latency = _conf.get(_section, 'port_high_latency')
	_port_low_latency = _conf.get(_section, 'port_low_latency')
	_meg_device_ip = _conf.get(_section, 'meg_device_ip')

	db = sql.connect("192.168.122.10","litadmin","litadmin123","LITdb")
        cursor = db.cursor()



    	# Spawn Threads
	if (_high_latency == 1) and (_low_latency == 1):
		print "ERROR -> Please select either HLL or LLL\n"
		sys.exit(0)
	elif _high_latency == 1:
		t0 = ZMQ_Client_HLL()
		t0.start()
		_thread_pool.append(t0)
	elif _low_latency == 1:
		t0 = ZMQ_Client_LLL()
		t0.start()
		_thread_pool.append(t0)
	else:
		print "ERROR -> Please select either HLL or LLL\n"

	t1 = LIT_DB_Thread(db,cursor)
        t1.start()
	_thread_pool.append(t1)

	
def _print_header():
	_marker = '-------------------------------------------'
        _n = '\n'
	print _n + _marker
	print "Process name:" + __file__ + _n
	print "Author: " + __author__ + _n 
	print "Copyright: " + __copyright__ + _n
	print "Version: " + __version__ + _n
	print _marker + _n
	return 

if __name__ == '__main__':
        main()

