

from COAP_queue import coap_queue
from time import *

coap = coap_queue()

while True:
    sleep(2)
    coap.get_lock()
    print (coap.get())
    coap.release_lock()
