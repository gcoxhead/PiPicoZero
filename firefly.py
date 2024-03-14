from picozero import pico_led, LED, Switch
from time import sleep

pico_led.on()
sleep(1)
pico_led.off()

firefly = LED(13) #Use GP13
switch = Switch(5) # Use GP18

while True:
    if switch.is_closed: #wires are connected
        firefly.on()
        sleep(0.5)
        firefly.off()
        sleep(2.5)
    else: #Wires not connected
        firefly.off()
        sleep(0.1) #Small delay
