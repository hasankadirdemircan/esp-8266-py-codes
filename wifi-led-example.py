import network
import socket
import machine

SSID = "Wifi_Name"
PASSWORD = "Wifi_Password"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    pass

print("connected, IP:", wifi.ifconfig()[0])

# LED pin
led = machine.Pin(4, machine.Pin.OUT)  # D2 = GPIO4

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("connected success:", addr)
    request = conn.recv(1024).decode()
    
    if "GET /on" in request:
        led.value(1)
        response = "LED open"
    elif "GET /off" in request:
        led.value(0)
        response = "LED close"
    else:
        response = "ESP8266 Web Sunucu"

    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + response)
    conn.close()

