import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
display = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
display.begin()

# Clear display.
display.clear()
display.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = display.width
height = display.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
getIP = "hostname -I | cut -d\' \' -f1"
getCPU = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
getRAM = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
getDisk = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
getTemp = "cat /sys/class/thermal/thermal_zone0/temp"
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    IP = subprocess.check_output(getIP, shell=True).decode('utf-8')
    CPU = subprocess.check_output(getCPU, shell=True).decode('utf-8')
    MemUsage = subprocess.check_output(getRAM, shell=True)
    Disk = subprocess.check_output(getDisk, shell=True)
    Temp = (subprocess.check_output(getTemp, shell=True).decode('utf-8'))[: -4]

    # Write two lines of text.

    draw.text((x, top), 'IP: {0}'.format(IP), font=font, fill=255)
    draw.text((x, top + 8), '{0} ({1}ºC)'.format(CPU, Temp), font=font, fill=255)
    draw.text((x, top + 16), MemUsage, font=font, fill=255)
    draw.text((x, top + 25), Disk, font=font, fill=255)

    # Display image.
    display.image(image)
    display.display()
    time.sleep(1)
