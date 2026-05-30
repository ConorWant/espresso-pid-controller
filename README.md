# espresso-pid-controller
A PID based espresso machine controller built on the Raspberry Pi Pico W. Designed to add precise temperature control, pressure profiling, a touchscreen UI and datalogging. 

## Features (planned)
 
- PID temperature control
- Pressure profiling
- Touchscreen UI
- Web dashboard and shot data logging
## Hardware
 
- Raspberry Pi Pico W
- MAX31855 thermocouple amplifier + K-type thermocouple
- Fotek SSR-40DA solid state relay
- XDB401 pressure transducer
- ILI9341 2.8" TFT touchscreen
## Status
 
Early development — hardware being sourced, architecture being planned.

## Repository Structure
 
```
espresso-pid-controller/
├── firmware/       # MicroPython code for the Pico W
├── dashboard/      # Web dashboard and data logging (Pi 4)
├── docs/           # Wiring diagrams and notes
├── hardware/       # 3D print files and enclosure designs
└── tests/          # Bench test scripts
```
 
## License
 
MIT
