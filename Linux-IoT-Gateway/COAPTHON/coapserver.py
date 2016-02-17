#!/usr/bin/env python

import getopt
import sys
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from exampleresources import BasicResource, Long, Separate, Storage, Big, voidResource, XMLResource, ETAGResource, Child, \
    MultipleEncodingResource



__author__ = 'giacomo'


class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast) 
        self.add_resource('basic/', BasicResource())
        self.add_resource('storage/', Storage())
        self.add_resource('separate/', Separate())
        self.add_resource('long/', Long())
        self.add_resource('big/', Big())
        self.add_resource('void/', voidResource())
        self.add_resource('xml/', XMLResource())
        self.add_resource('encoding/', MultipleEncodingResource())
        self.add_resource('etag/', ETAGResource())
        self.add_resource('child/', Child())

        self.host = host
        self.port = port

    def main_2(self):  # pragma: no cover

        server = CoAPServer(self.host, self.port)
        print "CoAP Server start on " + self.host + ":" + str(self.port)
        print self.root.dump()
        try:
            server.listen(10)
        except KeyboardInterrupt:
            print "Server Shutdown"
            server.close()
            print "Exiting..."


if __name__ == "__main__":  # pragma: no cover
    main_2(sys.argv[1:])
