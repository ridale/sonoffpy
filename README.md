# Setup
## Install esptool
Load the esptool on your computer
```
sudo pip install esptool
```
## clear flash
Power on the sonoff holding down the button
```
esptool.py --port /dev/ttyUSB0 erase_flash
```
## load firmware
Power on the sonoff holding down the button
```
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20171101-v1.9.3.bin
```

## check
Reboot the board and screen into the prompt
```
screen /dev/ttyUSB0 115200
```
You should see the REPL console
```
>>> import esp
>>> esp.check_fw()
```
## connect wifi
Connect to a hotspot to make things easier
```
>>> import network
>>> sta_if = network.WLAN(network.STA_IF)
>>> sta_if.scan()
>>> sta_if.connect('<your ESSID>', '<your password>')
>>> sta_if.ifconfig()
```
You should see your ip address etc, it may take a while to connect to the hotspot
## start webrepl
Start the webrepl server on the board
```
import webrepl_setup
```
Then follow the onscreen instructions
## get the client
```
git clone https://github.com/micropython/webrepl.git
```
And browse to the file location ...
```
file:///home/richard/sonoffpy/webrepl/webrepl.html
```
Then enter the IP address you saw above in the connect to wifi section
## load lib
in a repl prompt run
```
import upip
upip.install('uasyncio')
upip.install('uhttpd')
```
This installs the asyncio library allowing "multithreading" and the http server library

## check the hardware a bit...
We can do some IO tests
```
>>> import machine
>>> sw = machine.Pin(0, machine.Pin.IN)
>>> sw.value()
1
>>> sw.value()
0
```
When the button is pressed the switch pin goes low.

```
>>> led = machine.Pin(13, machine.Pin.OUT)
>>> led.on()
>>> led.off()
```

## load program
We can load a program that is run at startup by loading a file called main.py
