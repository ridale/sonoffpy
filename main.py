import machine
import network
import uhttpd
import uasyncio as asyncio
import config


led    = None
relay  = None
button = None

on_handler      = None
off_handler     = None
status_handler  = None

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
        
        await asyncio.sleep(1)


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
    on_handler = 
    off_handler = 
    status_handler = 
    
def main_loop():
    '''Main run loop'''
    setup()
    loop = asyncio.get_event_loop()
    loop.create_task(check_inputs())
    server = uhttpd.Server([
                    ('/on',  on_handler),
                    ('/off', off_handler),
                    ('/',    status_handler)
                    ])
    server.run()
    teardown()


if __name__ == '__main__':
    setup()
    try:
        main_loop()
    finally:
        teardown()
