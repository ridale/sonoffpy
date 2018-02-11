import machine
import network


PIN_BUTTON = const(0)
PIN_RELAY  = const(12)
PIN_LED    = const(13)

led    = None
relay  = None
button = None

def check_inputs():
    '''Check the digital IO and set the relay accordingly
    
    TODO figure out which sense the relay is
    '''
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

def do_webstuff():
    '''Handle any webserver requests'''


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
    iface.connect('SSID','PASSWORD')

def main_loop():
    '''Main runloop should never exit'''
    while 1:
        # do the things
        check_inputs()
        do_webstuff()

if __name__ == '__main__':
    setup()
    try:
        main_loop()
    finally:
        teardown()
