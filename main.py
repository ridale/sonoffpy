import sys
import machine
import network
import uhttpd
import utime
import uhttpd.api_handler
import uasyncio as asyncio
import logging

SSID='yourssid'
PASSWORD='yourpassword'

PIN_BUTTON = const(0)
PIN_RELAY  = const(12)
PIN_LED    = const(13)

button = machine.Pin(PIN_BUTTON, machine.Pin.IN)
relay  = machine.Pin(PIN_RELAY,  machine.Pin.OUT)
led    = machine.Pin(PIN_LED,    machine.Pin.OUT)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("sonoffpy")


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
    log.critical("Exiting sonoffpy")
    # disconnect
    # relay off

def setup():
    '''Setup the system (run once at start)'''
    log.info("Started - setup hardware")
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
            log.critical('Connecting to WLAN timed out. Resetting!')
            machine.reset()



def main_loop():
    '''Main run loop'''
    log.info("get loop")
    loop = asyncio.get_event_loop()
    log.info("make server")
    # setup webserver
    handler = uhttpd.api_handler.Handler([([], Handler())])
    server = uhttpd.Server([('/', handler)])
    log.info("add task")
    loop.create_task(check_inputs())
    log.info("run server")
    server.run()


if __name__ == '__main__':
    setup()
    try:
        main_loop()
    except Exception as exp:
        sys.print_exception(exp)
    finally:
        teardown()
