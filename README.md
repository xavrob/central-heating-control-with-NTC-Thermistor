# central heating control with NTC-Thermistor and ADS1015
## Hardware
### OLED display of NTC temperature through ADS1x15 converter
### Adafruit 128x64 OLED Bonnet for Raspberry Pi, PRODUCT ID: 3531 
not yet
### Adafruit ADS1015 12-Bit ADC - 4-kanaals met programmeerbare Gain Amplifier, PRODUCT ID: 1083 
(https://www.adafruit.com/product/1083)
### Adafruit 10K Precision Epoxy Thermistor - 3950 NTC, PRODUCT ID: 372
(https://www.adafruit.com/product/372)
### Relais
(https://www.kiwi-electronics.nl/nl/4-kanaals-5v-relais-module-1330)
(https://www.youtube.com/watch?v=My1BDB1ei0E)
## Software
### Python
CV-regeling.py
 E:\Raspberry Pi\Temp\CV-regeling.xlsx
 -5°C = 40Kohm
 0°C  = 32Kohm
 10°C = 20Kohm
 19°C = 13Kohm
 25°C = 10Kohm
 43°C = 4,7Kohm

 vanaf 3,5 minuut gaat de CV over naar "hoog vermogen / laag rendement" van "3" naar "5"
 de CV slaat normaal ongeveer 3 x langer aan dan de tijd van de puls
 de CV verbruikt dan ongeveer 60 liter gas per minuut puls, of 20 liter gas per minuut "branden"
 per minuut branden, dus "3 = hoog rendement/ laag vermogen" verbruikt de CV 20 liter/minuut
 bij de instelling van de LOGO bleef de CV "3 = hoog rendement/ laag vermogen" 
  als er 5 minuten tussen het begin van de pulsen was.

 de LOGO was zo ingesteld dat er elke 5 min een puls was van 2 min
  dwz 12 pulsen/uur om "3 = hoog rendement/ laag vermogen" te krijgen
 indien na één uur de vraag nog steeds is, wordt het aantal pulsen verhoogd,
  dwz dat men dan tijdelijk "5 = laag rendement/ hoog vermogen" krijgt

 1m³ = 8 pulsen of 125 liter per puls hoog rendement/ laag vermogen ...



 100 meter kabel heeft een weerstand van 14 Ohm
 10 meter kabel heeft geen invloed op de weerstand
 10 meter kabel = 20 meter stroomdraad van en naar de 10K Ohm NTC Epoxy Thermistor
 dus 2,8 Ohm extra
 https://www.adafruit.com/product/372
 adefruit product 372 : 10K Ohm NTC Epoxy Thermistor

 https://www.adafruit.com/product/1083
 ADS1015 12-Bit ADC - 4 Channel I2C
 adefruit PRODUCT ID: 1083

 relais
 https://www.youtube.com/watch?v=My1BDB1ei0E
 4-kanaals 5V relais module : kw-1613
 remove jumper and use pins, under jumper, for connecting separatly 5V and 3.3V
 don't use the VCC of the 6-pins GND,IN1,IN2,IN3,IN4,(VCC)
 JD-VCC = 5V
 VCC    = 3.3V
 pin directly to IN1 or 2 or 3 or 4 without resistance
