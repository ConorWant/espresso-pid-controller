from machine import SPI, Pin
import time

spi = SPI(0, baudrate=5000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)
cs.value(1)

while True:
    cs.value(0)
    data = spi.read(4)
    cs.value(1)
    
    # Check for error bit
    if data[3] & 0x01:
        print("Error - check thermocouple connection")
    else:
        temp = ((data[0] << 8 | data[1]) >> 2) * 0.25
        print(f"{temp:.1f} °C")
    
    time.sleep(1)
        
