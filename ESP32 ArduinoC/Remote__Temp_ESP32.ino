/*
 * ildrummer
 * Oct 2020
 * 
 * Use an ESP32-CAM with a DS18B20 waterproof temperature probe to collect
 * ambient room temperature.
 * 
 * ESP32-CAM hosts a web server and provides JSON-packaged temperature data 
 * from a custom REST API.
 * 
 * ESP32 will reset once per day
 * 
 * Future improvements:
 *  - check for WiFi connectivity every minute and reconnect as needed.
 *  - store errors in a log file or buffer
 *  - add REST functions to report uptime, transmit the log buffer, and 
 * */
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <time.h>

// 86400000 for 24 hours
unsigned long resetInterval = 86400000;

// GPIO where the DS18B20 is connected to
const int oneWireBus = 13;     

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

// WiFi parameters
const char *wifiName = "network_name";
const char *password = "******";
IPAddress local_IP(192, 168, 1, 12);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0); 


WebServer server(80);
StaticJsonDocument<250> jsonDoc;
char buffer[250];

void connectToWifi(){
  Serial.print("Connecting to ");
  Serial.println(wifiName);
  
  if (!WiFi.config(local_IP, gateway, subnet)){
    Serial.println("Static IP failed to configure");
  }
  
  WiFi.begin(wifiName, password);
  while (WiFi.status() != WL_CONNECTED){
    delay (500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("WiFi ready. Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
}

void setupServer() {
  server.on("/temperature", getTempF);
  server.begin();
}

void getTempF() {
  Serial.println("Get temperature");
  create_json("Temperature", getTempValueF());
  server.send(200, "application/json", buffer);
}


void create_json(char *tag, float value){
  jsonDoc.clear();
  jsonDoc["type"] = tag;
  jsonDoc["value"] = value;
  serializeJson(jsonDoc, buffer);
}

void setup() {
  // Start the Serial Monitor
  Serial.begin(115200);
  Serial.println("I'm back online");

  pinMode(oneWireBus, OUTPUT); 
  
  connectToWifi();

  pinMode(oneWireBus, INPUT);

  setupServer();
  
  // Start the DS18B20 sensor
  sensors.begin();

}


float getTempValueF(){ 
  sensors.requestTemperatures(); 
  sensors.getTempFByIndex(0);
}
float getTempValueC(){
  sensors.requestTemperatures(); 
  sensors.getTempFByIndex(0);
}



void loop() {
  server.handleClient();
  Serial.print("Temp: ");
  Serial.println(getTempValueF());
  delay(2000);

  // Reset once per interval (default to once/day)
  if (millis() > resetInterval){
    restart();
  }
}

void restart (){
  Serial.println("Restarting");
  ESP.restart();
}
