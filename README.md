# Custom USB Game Controller (HID Emulation Bridge)
A hardware-software hybrid project developed for the Data and Logic Design(DLD) semester course. This project implements a fully functional game controller using an Arduino Mega 2560, utilizing a Python-based serial bridge to translate analog signals into system-level HID (Human Interface Device) inputs.
Due to hardware constraints with native HID support on the ATmega2560, I engineered a Python-based communication bridge to translate Serial data into virtual controller inputs, ensuring low-latency gameplay.
## Hardware Stack
- **Microcontroller:** Aduino Maga 2560
- **Input Module:** 2x 5-pin joystick(X/Y Axis + Select Button)
- **Digital Inputs:** 4x Tactile Push Buttons(Mapped to actions buttons)
- **Prototyping:** BreadBoard and Jumper wires
- **Interface:** USB 2.0 type A/B cable
## Software & Libraries
- **Embeded:** Arduino IDE(C++)
- **Communication:** Serial Port (9600/115200 baud)
- **Bridge Script:** Python
- **Python Libraries:**
  - pyserial (for data aaquicisition)
  - Pynput
## Logic & Implementation
1. **Signal Aquicisition:** The Arduino polls analog values from the joysticks ($0$ to $1023$) and digital states from the buttons.
2. **Data Processing:** To ensure stability, the firmware applies a **deadzone** to the analog sticks to prevent "stick drift" in the serial stream.
3. **Serial Mapping:** Data is packetized into a comma-separated string and transmitted via the USB-Serial buffer.
4. **Python Bridge:** The host-side script parses the incoming serial packets and maps them to virtual keyboard/controller events in real-time.
## Instalation & Setup
1. Upload the .ino sketch to your Mega 2560
2. Run pip install pyserial
3. Plug in the controller and run keyboard_controller.py
4. The Pc will now recognize the breadboard circuit as a standard game controller.

