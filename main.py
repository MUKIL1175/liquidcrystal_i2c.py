from machine import Pin, I2C
from liquidcrystal_i2c import I2cLcd

# Initialize I2C on ESP32 pins SDA=21, SCL=22
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Check your LCD I2C address with an I2C scan (commonly 0x27 or 0x3F)
lcd = I2cLcd(i2c, 0x27, 2, 16)

lcd.clear()
lcd.set_cursor(0, 0)
lcd.write_string("Hello")
lcd.set_cursor(0, 1)
lcd.write_string("ESP32 + LCD")

