# Remote Temperature Sensor System

My house is not a consistent temperature and I don't know why (well, counting the number of vents gives me a clue...).  To find out the scale of the temperature differential and how if related to my furnace heating cycles, I'm developing this application.

## Strategy
1. Collect temperature data
2. Store data in a SQLite database
3. Pull data from database and graph 

## Techniques
1. Test-driven development using PyTest
2. Multithreading (ESP32-CAMs are slooooow)

# Implementation
1. ESP-32 CAM with DS18B20 waterproof temperature sensor on breadboard.  Microcontroller programmed with file in ESP32 ArduinoC/Remote_Temp_ESP32.ino


# To Do
## Inversion of Control
1. Data Access Object pattern for DB
2. Sensor interface for temp sensors

## Dependency Injection for Testing
