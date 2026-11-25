from machine import SPI, Pin
import time

spi = SPI(0, baudrate=5000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)
cs.value(1)

def read_temperature():
    cs.value(0)
    data = spi.read(4)
    cs.value(1)
    if data[3] & 0x01:
        return None
    return ((data[0] << 8 | data[1]) >> 2) * 0.25

while True:
    temp = read_temperature()
    if temp is not None:
        print("Temp: {}C".format(temp))
    else:
        print("Error reading thermocouple")
    time.sleep(1)
