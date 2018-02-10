import machine

PIN_BUTTON = const(0)
PIN_RELAY  = const(12)
PIN_LED    = const(13)

led    = None
relay  = None
button = None

def teardown():
    # oops alert
    # disconnect
    # relay off

def setup():
    # setup IO
    button = machine.Pin(PIN_BUTTON, machine.Pin.IN)
    relay  = machine.Pin(PIN_RELAY,  machine.Pin.OUT)
    led    = machine.Pin(PIN_LED,    machine.Pin.OUT)
    # connect to wifi


def main_loop():
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
