# Remote Temperature Sensor System

My house is not a consistent temperature and I don't know why (well, counting the number of vents gives me a clue...).  To find out the scale of the temperature differential and how if related to my furnace heating cycles, I'm developing this application.

## Strategy
1. Collect temperature data
2. Store data in a SQLite database
3. Pull data from database and graph 

## Techniques
1. Test-driven development using PyTest
2. Multithreading (ESP32-CAMs are slooooow)
3. Containerization to handle application resilience (restart on failure)

# Implementation

## Hardware
1. ESP-32 CAM microcontroller with DS18B20 waterproof temperature sensor on breadboard.  See this [Random Nerd Tutorials article](https://randomnerdtutorials.com/esp32-ds18b20-temperature-arduino-ide/). 
2. Rasperry Pi 3 running the temperature server 24/7.

## Software
1. ESP-32 programmed with file in [/ESP32_ArduinoC/Remote_Temp_ESP32.ino](/ESP32_ArduinoC/Remote_Temp_ESP32.ino).  Runs as a REST endpoint and serves JSON temperature data.
2. SQLite3 database to store temperature data, sensors
3. Python server that polls all sensors for data and stores the temperatures returned.
4. Docker container encapsulating Python server and database.
