import network
import time
from machine import SPI, Pin, ADC
from umqtt.simple import MQTTClient
from config import WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)
while not wlan.isconnected():
    time.sleep(0.5)
print("WiFi connected:", wlan.ifconfig()[0])

# MAX31855 thermocouple
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

# HX711 load cell
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

# Pressure transducer on GP26
pressure_adc = ADC(Pin(26))
DIVIDER_RATIO = 5100 / 15100
VREF = 3.3

def read_pressure_bar():
    raw = pressure_adc.read_u16()
    voltage_at_pin = (raw / 65535) * VREF
    voltage_at_transducer = voltage_at_pin / DIVIDER_RATIO
    psi = (voltage_at_transducer - 0.5) * (200 / 4.0)
    return psi * 0.0689476

hx = HX711(data_pin=14, clock_pin=15)
print("Taring...")
time.sleep(2)
hx.tare()

client = MQTTClient("pico", MQTT_BROKER)
client.connect()
print("MQTT connected")

while True:
    temp = read_temperature()
    weight = hx.get_grams()
    pressure = read_pressure_bar()

    if temp is not None:
        client.publish("espresso/temperature", "{:.2f}".format(temp))
    client.publish("espresso/weight", "{:.1f}".format(weight))
    client.publish("espresso/pressure", "{:.2f}".format(pressure))

    print("Temp: {}C  Weight: {}g  Pressure: {:.2f} bar".format(temp, weight, pressure))
    time.sleep(1)