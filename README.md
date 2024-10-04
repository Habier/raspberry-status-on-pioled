# Raspberry's status on 128_32 piOled

Click [here](https://github.com/adafruit/Adafruit_Python_SSD1306) to visit original Adafruit's repository which contains
more examples  
This is a personalized version of the script  
The oled screen will display IP, CPU load, Memory Usage, Disk usage and CPU temperature

# Requirements

```shell
sudo apt-get install libopenjp2-7
```

You will need to enable i2c

```shell
sudo raspi-config
```

# Run as service

```shell
sudo nano /etc/systemd/system/oled-status.service
```

```text
[Unit]
Description=Python Script for OLED Status Display
After=network.target

[Service]
ExecStart=/home/pi/oled-status/venv/bin/python3 /home/pi/oled-status/start.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Now Enable and run it

```shell
sudo systemctl daemon-reload && sudo systemctl enable oled-status.service && sudo systemctl start oled-status.service
```