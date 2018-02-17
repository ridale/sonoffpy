# Setup
These instructions have been tested on a Linux PC running Ubuntu 16.04, your mileage may vary.

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
import network
sta_if = network.WLAN(network.STA_IF)
sta_if.scan()
sta_if.connect('<your ESSID>', '<your password>')
sta_if.ifconfig()
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
mkdir ~/github
cd ~/github
git clone https://github.com/micropython/webrepl.git
```
And browse to the file location ...
```
file:///home/user/github/webrepl/webrepl.html
```
Then enter the IP address you saw above in the connect to wifi section

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

## Build firmware
We need to build the micropython firmware as there is not enough RAM to compile the program to bytecode on the device so we will need to add the libraries to the firmware build.

As with all of the source we get in this project it is cloned into the ~/github directory

### build SDK
First we need the extensa SDK to be able to build the firmware for the esp8266
```
cd ~/github
git clone https://github.com/pfalcon/esp-open-sdk.git
cd esp-open-sdk
```
Then we need the build tools, these are listed in the esp-open-sdk reaedme
```
sudo apt-get install make unrar-free autoconf automake libtool gcc g++ gperf \
    flex bison texinfo gawk ncurses-dev libexpat-dev python-dev python python-serial \
    sed git unzip bash help2man wget bzip2
```
Then we build the sdk tools
```
make
```

### build micropython
Now that we have the build tools ready we can use them to build the firmware. We are not going to add the extra libraries yet, if anything goes wrong here we know it is not to do with the things we added!
```
cd ~/github
git clone https://github.com/micropython/micropython.git
cd micropython
git pull --tags
git submodule update --init
make -C  mpy-cross
cd ports/esp8266
make axtls
make
```

### include libs
Now that we know that the firmware can build on our computer we can add the extra libraries we need to bake into the firmware.
```
cd ~/github
git clone https://github.com/micropython/micropython-lib.git
cd ~/github
git clone https://github.com/fadushin/esp8266.git
```
Now we want to symlink the library modules we are interested in into the build directory for the firmware ```~/github/micropython/ports/esp8266/modules```
```
cd ~/github/micropython/ports/esp8266/modules
ln -s ~/github/micropython-lib/uasyncio/uasyncio uasyncio
ln -s ~/github/micropython-lib/uasyncio.core/uasyncio/core.py uasyncio/
ln -s ~/github/esp8266/micropython/uhttpd/uhttpd/ uhttpd
```
Now if we remake our firmware we will get the frozen modules required
```
cd ~/github/micropython/ports/esp8266
make
```

## load program
**NOTE** This code is currently a Work In Progress and it is likely that it does not yet work.

First you will want to edit the config.py file and add your wifi SSID and password. Then load the program to be run at startup by uploading the main.py and config.py files to the sonoff using the webrepl upload button.
