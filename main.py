import machine
import network
import uhttpd
import uhttpd.api_handler
import uasyncio as asyncio
import config


led    = None
relay  = None
button = None

handler      = None

class Handler:
    def __init__(self):
        pass

    #
    # callbacks
    #
    def get(self, api_request):
        components = api_request['context']
        if (components == 'on'):
            relay.off()
            led.off()
        elif (components == 'off'):
            relay.on()
            led.on()

        if (relay.off()):
            return {'state':'on'}
        else:
            return {'state':'on'}

def check_inputs():
    '''Check the digital IO and set the relay accordingly

    TODO figure out which sense the relay is
    '''
    while True:
        change_relay = False
        while (button.value() == 0):
            # button pressed
            change_relay = True
        
        if (change_relay):
            if(relay.value() == 1):
                relay.off()
            else:
                relay.on()
        
        if (relay.value() == 0):
            led.off() # is on
        else:
            led.on()  # is off
        
        await asyncio.sleep_ms(200)


def teardown():
    '''Should never be run'''
    # oops alert
    # disconnect
    # relay off

def setup():
    '''Setup the system (run once at start)'''
    # setup IO
    button = machine.Pin(PIN_BUTTON, machine.Pin.IN)
    relay  = machine.Pin(PIN_RELAY,  machine.Pin.OUT)
    led    = machine.Pin(PIN_LED,    machine.Pin.OUT)
    # connect to wifi
    iface = network.WLAN(network.STA_IF)
    iface.connect(SSID,PASSWORD)
    # setup webserver
    handler = uhttpd.api_handler.Handler([([], Handler())])


def main_loop():
    '''Main run loop'''
    setup()
    loop = asyncio.get_event_loop()
    loop.create_task(check_inputs())
    server = uhttpd.Server([('/', status_handler)])
    server.run()
    teardown()


if __name__ == '__main__':
    setup()
    try:
        main_loop()
    finally:
        teardown()
