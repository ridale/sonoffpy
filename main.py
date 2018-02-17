'''
Seems to work mosty, need to check the sense of the relay
all of the other I/O is reversed.
'''
import machine
import network
import utime
import uhttpd
import uhttpd.api_handler
import uasyncio as asyncio

SSID = 'yourssid'
PASSWORD = 'yourpassword'


PIN_BUTTON = const(0)
PIN_RELAY  = const(12)
PIN_LED    = const(13)

button = machine.Pin(PIN_BUTTON, machine.Pin.IN)
relay  = machine.Pin(PIN_RELAY,  machine.Pin.OUT)
led    = machine.Pin(PIN_LED,    machine.Pin.OUT)

class Handler:
    def __init__(self):
        pass

    #
    # callbacks
    #
    def get(self, api_request):
        components = api_request['context']
        if (components[0] == 'on'):
            relay.off()
            led.off()
        elif (components[0] == 'off'):
            relay.on()
            led.on()
        # return
        if (relay.value() == 0):
            return {'state':'on'}
        else:
            return {'state':'off'}

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
    print("Exiting")
    # disconnect
    # relay off
    # reboot
    machine.reset()

def setup():
    '''Setup the system (run once at start)'''
    # setup IO
    relay.on()
    led.on()
    # connect to wifi
    start_ms = utime.ticks_ms()
    iface = network.WLAN(network.STA_IF)
    iface.connect(SSID,PASSWORD)
    while not iface.isconnected():
        utime.sleep_ms(100)
        if utime.ticks_diff(start_ms, utime.ticks_ms()) > 10000:
            print('Connecting timed out!')
            machine.reset()


def main_loop():
    '''Main run loop'''
    loop = asyncio.get_event_loop()
    # setup webserver
    handler = uhttpd.api_handler.Handler([([], Handler())])
    server = uhttpd.Server([('/', handler)])
    loop.create_task(check_inputs())
    server.run()

if __name__ == '__main__':
    setup()
    try:
        main_loop()
    finally:
        teardown()
