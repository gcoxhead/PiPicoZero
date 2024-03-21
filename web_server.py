import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led, LED
import machine

ssid = 'VM7274398'
password = 'tn5Qpstxz7fx'

redLED = LED(2) # Use GP2
insideTemp = 0
humidity = 0

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(processorTemp, insideTemp, state, humidity):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            
            </form>
            
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            
            </form>
            
            <form action="./redlighton">
            <input type="submit" value="Red Light on" />
            </form>
            
            
            <form action="./redlightoff">
            <input type="submit" value="Red Light off" />
            </form>
            
            
            
            <p>LED is {state}</p>
            <p>Processor Temperature is {processorTemp}</p>
            <p>Inside Temperature is {insideTemp}</p>
            <p>Humidity is {humidity}</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    processorTemp = 0
    insideTemp = 0
    humidity = 0
    
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state ='ON'
        elif request =='/lightoff?':
            pico_led.off()
            state='OFF'
        elif request == '/redlighton?':
            redLED.on()
        elif request == '/redlightoff?';
            redLED.off()
            
        processorTemp = pico_temp_sensor.temp
        print(request)
        
        html = webpage(temperature, state)
        client.send(html)
        client.close()
try:
    ip = connect()
    connection = open_socket(ip)
    serve (connection)
    
except KeyboardInterrupt:
    machine.reset()