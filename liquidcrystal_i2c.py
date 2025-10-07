# liquidcrystal_i2c.py
# MicroPython driver for 1602/2004 I2C LCD displays
# Compatible with ESP32/ESP8266
#By Monamukil SS

from machine import I2C
from time import sleep_ms

# LCD Commands
LCD_CLR = 0x01
LCD_HOME = 0x02
LCD_ENTRY_MODE = 0x04
LCD_DISPLAY_CTRL = 0x08
LCD_SHIFT = 0x10
LCD_FUNCTION = 0x20
LCD_SET_CGRAM = 0x40
LCD_SET_DDRAM = 0x80

# Flags for display entry mode
LCD_ENTRY_LEFT = 0x02
LCD_ENTRY_SHIFT_DECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAY_ON = 0x04
LCD_CURSOR_ON = 0x02
LCD_BLINK_ON = 0x01

# Flags for function set
LCD_4BIT_MODE = 0x00
LCD_2LINE = 0x08
LCD_5x8DOTS = 0x00

# Backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

# Enable bit, Read/Write, Register Select
En = 0b00000100
Rw = 0b00000010
Rs = 0b00000001


class I2cLcd:
    """MicroPython I2C LCD driver (1602 / 2004)"""

    def __init__(self, i2c: I2C, i2c_addr: int, num_lines: int = 2, num_columns: int = 16):
        self.i2c = i2c
        self.addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = LCD_BACKLIGHT

        self._init_lcd()

    def _write_byte(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.backlight]))

    def _toggle_enable(self, data):
        sleep_ms(1)
        self._write_byte(data | En)
        sleep_ms(1)
        self._write_byte(data & ~En)
        sleep_ms(1)

    def _send(self, data, mode=0):
        high = data & 0xF0
        low = (data << 4) & 0xF0
        self._write4bits(high | mode)
        self._write4bits(low | mode)

    def _write4bits(self, data):
        self._write_byte(data)
        self._toggle_enable(data)

    def _command(self, cmd):
        self._send(cmd, 0)

    def write_char(self, char):
        self._send(ord(char), Rs)

    def write_string(self, string):
        for char in string:
            self.write_char(char)

    def clear(self):
        self._command(LCD_CLR)
        sleep_ms(2)

    def home(self):
        self._command(LCD_HOME)
        sleep_ms(2)

    def set_cursor(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row > self.num_lines:
            row = self.num_lines - 1
        self._command(LCD_SET_DDRAM | (col + row_offsets[row]))

    def backlight_on(self):
        self.backlight = LCD_BACKLIGHT
        self._write_byte(0)

    def backlight_off(self):
        self.backlight = LCD_NOBACKLIGHT
        self._write_byte(0)

    def _init_lcd(self):
        sleep_ms(50)
        self._write4bits(0x30)
        sleep_ms(5)
        self._write4bits(0x30)
        sleep_ms(1)
        self._write4bits(0x20)

        self._command(LCD_FUNCTION | LCD_2LINE | LCD_5x8DOTS | LCD_4BIT_MODE)
        self._command(LCD_DISPLAY_CTRL | LCD_DISPLAY_ON)
        self._command(LCD_CLR)
        self._command(LCD_ENTRY_MODE | LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT)
        sleep_ms(2)
