#https://aiocoap.readthedocs.org/en/latest/examples.html
#!/usr/bin/python3

#For DEBUG information just like printf
import logging

#For co-routines
import asyncio

#For Coap communication
import aiocoap

#For [resource: infomation block] for different sensor nodes, time, pressure, light etc. 
import aiocoap.resource as resource

from COAP_queue import coap_queue

#	Block Data Transfer Class / Resource Creation named as block to save large data.
 
class BlockResource(resource.Resource):
    """
    Example resource which supports GET and PUT methods. It sends large
    responses, which trigger blockwise transfer.
    """

    def __init__(self):
        super(BlockResource, self).__init__()
        self.content = ("This is the resource's default content. It is padded "\
                "with numbers to be large enough to trigger blockwise "\
                "transfer.\n" + "0123456789\n" * 100).encode("ascii")

# For tackling GET command by the client
    @asyncio.coroutine
    def render_get(self, request):
        response = aiocoap.Message(code=aiocoap.CONTENT, payload=self.content)
        return response

# For tackling PUT command by the client
    @asyncio.coroutine
    def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        payload = ("I've accepted the new payload. You may inspect it here in "\
                "Python's repr format:\n\n%r"%self.content).encode('utf8')
        th = request.payload
        TH = int(th.decode("utf-8"))
        print ('Threshold = %d' % TH)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)


class GWResource(resource.ObservableResource):
    """
    Example resource that can be observed. The `notify` method keeps scheduling
    itself, and calles `update_state` to trigger sending notifications.
    """
    def __init__(self):
        super(GWResource, self).__init__()

        self.notify()
        
    def notify(self):
        self.updated_state()
        asyncio.get_event_loop().call_later(10, self.notify)

    # For tackling PUT command by the client
    @asyncio.coroutine
    def render_put(self, request):
        queue = coap_queue()
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        payload = ("I've accepted the new payload. You may inspect it here in "\
                "Python's repr format:\n\n%r"%self.content).encode('utf8')
	
        payl = request.payload
        payl = payl[:-1]
        print ("Lock has been Acquired!!!")
        queue.get_lock()
        queue.put(payl)
        print ("Write Data to Queue = ")
        print (payl)
        #print (queue.get())
        queue.release_lock()
        print ("Lock has been Released!!!")

        return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)


    @asyncio.coroutine
    def render_get(self, request):        
        payload = "20".encode('utf8')           
        return aiocoap.Message(code=aiocoap.CONTENT, payload=payload)
                


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation . It is for registering the resources.
    root = resource.Site()

    # Add resources to the tree and get register by object root.

    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(('other', 'block'), BlockResource())

    root.add_resource(('gw',), GWResource())

    asyncio.async(aiocoap.Context.create_server_context(root))     #For scheduling co-routines.   

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
