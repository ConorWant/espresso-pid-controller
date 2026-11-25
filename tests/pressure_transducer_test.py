from machine import ADC, Pin
import time

pressure_adc = ADC(Pin(26))
DIVIDER_RATIO = 5100 / 15100
VREF = 3.3

def read_pressure_bar():
    raw = pressure_adc.read_u16()
    voltage_at_pin = (raw / 65535) * VREF
    voltage_at_transducer = voltage_at_pin / DIVIDER_RATIO
    psi = (voltage_at_transducer - 0.5) * (200 / 4.0)
    return psi * 0.0689476

while True:
    pressure = read_pressure_bar()
    print("Pressure: {:.2f} bar".format(pressure))
    time.sleep(1)
