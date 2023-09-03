# Capacitive Foot Pressure Sensor Data Acquisition System

This repository contains the source code and documentation for a capacitive foot pressure sensor data acquisition system. The system is designed around the ESP32 microcontroller and utilizes 4 MDC04 chips to collect data from 16 channels of capacitance values. The collected data is transmitted via Bluetooth Low Energy (BLE) to a mobile phone's host computer app, and simultaneously recorded in a CSV file stored in the ESP32's FLASH memory. This project is primarily intended for capacitive foot pressure sensor applications but can also be adapted for other use cases that require wireless capacitance data acquisition.

## Features

- Utilizes ESP32 as the master controller.
- Collects capacitance values from 16 channels using 4 MDC04 chips.
- Transmits data to a mobile phone's host computer app via BLE.
- Records data in a CSV file on the ESP32's FLASH memory.
- Supports a burn-in interface for the ESP32 on the circuit board.
- USB interface for power supply (compatible with 5V battery modules).

## Getting Started

To set up and run this system, follow these steps:

1. **Hardware Setup**: Assemble the hardware components, including the ESP32 microcontroller and the 4 MDC04 chips. Ensure that the ESP32 burn-in interface and USB power supply interface are correctly connected.

2. **Programming**: The ESP32 is programmed using MicroPython. Run the `Read_cap.py` file on the ESP32, and make sure all the necessary support files have been imported into the main file.

3. **Android App**: The Android host computer app is developed using [APP Inventor](https://appinventor.mit.edu/). It provides the following features:
   - Displays pressure levels using colored blocks.
   - Real-time change curve.
   
4. **Connecting to the App**: After connecting a battery to the board and powering it up, follow these steps to connect to the Android app:
   - Open the app on your Android device.
   - Scan for BLE devices within the app.
   - Click on the device named "Remote_cap_meter" to connect.
   - Once connected, real-time data will be displayed in the app.

## Repository Contents

- `Read_cap.py`: Main program for the ESP32 written in MicroPython.
- Support files: Additional files necessary for the ESP32 program.
- Android App: Source code for the Android app developed with APP Inventor.
- Documentation: Additional documentation and resources.

## Usage

For detailed instructions on using the system, refer to the documentation provided in this repository.

## License

This project is licensed under the [MIT License](LICENSE).
