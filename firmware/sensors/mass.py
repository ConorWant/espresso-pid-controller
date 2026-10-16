from machine import Pin
import time

class HX711:
    def __init__(self, data_pin, clock_pin):
        self.pdat = Pin(data_pin, Pin.IN)
        self.psck = Pin(clock_pin, Pin.OUT)
        self.psck.value(0)
        self.tare_offset = 0
    
    def read(self):
        while self.pdat.value() == 1:
            pass
        
        count = 0
        for _ in range(24):
            self.psck.value(1)
            count = (count << 1) | self.pdat.value()
            self.psck.value(0)
        
        self.psck.value(1)
        self.psck.value(0)
        
        if count & 0x800000:
            count -= 0x1000000
        
        return count
    
    def tare(self):
        samples = [self.read() for _ in range(10)]
        self.tare_offset = sum(samples) // len(samples)
        print("Tared")
    
    def get_grams(self, scale_factor=1068):
        return (self.read() - self.tare_offset) / scale_factor

hx = HX711(data_pin=14, clock_pin=15)

print("Taring scale - remove anything from load cell...")
time.sleep(2)
hx.tare()

print("Ready")
while True:
    grams = hx.get_grams()
    print("{:.1f} g".format(grams))
    time.sleep(0.5)
