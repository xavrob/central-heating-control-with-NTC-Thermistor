# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
import tempmodule_a

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP


# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)


while True:
    if button_A.value:  # button is released
#        draw.ellipse((70, 40, 90, 60), outline=255, fill=0)  # A button
        print("a off")
        time.sleep(1)
        pass
    else:  # button is pressed:
#        draw.ellipse((70, 40, 90, 60), outline=255, fill=1)  # A button filled
#        disp.fill(0)
#        disp.show()
        font = ImageFont.truetype("FreeMonoBold.ttf", size=15)
#        temp_living = tempmodule.graden(1)
        temp_living = tempmodule_a.weerstand(1)
        print('1 : ',temp_living)
#        temp_water = tempmodule.graden(2)
        temp_water = tempmodule_a.weerstand(2)
        print('2 : ',temp_water)
#        temp_living = tempmodule.graden(3)
        temp_retour = tempmodule_a.weerstand(3)
        print('3 : ',temp_retour)
#        temp_living = tempmodule.graden(4)
        temp_buiten = tempmodule_a.weerstand(4)
        print('4 : ',temp_buiten)
#        text1= "living : %s°c " % (temp_living)
        text1= "living : %4.1f°c " % (temp_living)
        text2= "water  : %4.1f°c " % (temp_water)
        text3= "retour : %4.1f°c " % (temp_retour)
        text4= "buiten : %4.1f°c " % (temp_buiten)
        draw.text((1,1),text1,font=font,fill=255,)
        draw.text((1,17),text2,font=font,fill=255,)
        draw.text((1,33),text3,font=font,fill=255,)
        draw.text((1,49),text4,font=font,fill=255,)
        disp.image(image)
        disp.show()
        print("a on")
        time.sleep(10)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
#        disp.fill(0)
        disp.image(image)
        disp.show()
        time.sleep(10)
 
#    if button_B.value:  # button is released
#        draw.ellipse((70, 40, 90, 60), outline=255, fill=0)  # A button
#        print("b off")
#        pass
#        disp.fill(0)
#        disp.show()
#    else:  # button is pressed:
#        draw.ellipse((70, 40, 90, 60), outline=255, fill=1)  # A button filled
#        print("b on")
#        draw.rectangle((0, 0, width, height), outline=0, fill=0)
#        disp.fill(0)
#        disp.image(image)
#        disp.show()
#        time.sleep(10)


#    if not button_A.value and not button_B.value and not button_C.value:
#        catImage = Image.open("happycat_oled_64.ppm").convert("1")
#        disp.image(catImage)
#    else:
        # Display image.
