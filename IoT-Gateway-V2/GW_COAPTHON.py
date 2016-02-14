import sys
sys.path.insert(0, '/home/ahmer/Ahmer/Techknox/Python_Exercises/IoT-Gateway-V2/coapthon/')
from coapthon.server.coap import CoAP
from coapserver import CoAPServer
from COAP_queue import coap_queue
from time import *
import threading




class start_coap(threading.Thread):
	def __init__(self,ip,port,multicast):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.multicast=multicast
		global _data

	def run(self):
                while True:
                        sleep(1)
                        coap = CoAPServer(self.ip,self.port,self.multicast)
                        print "Entering"
                        coap.main_2()
                        print "Leaving"
                
                        
