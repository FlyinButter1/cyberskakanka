#  Raspberry Pi Master for Arduino Slave
#  i2c_master_pi.py
#  Connects to Arduino via I2C
  
#  DroneBot Workshop 2019
#  https://dronebotworkshop.com

from smbus2 import SMBus
import serial
import math
import struct
import time
import board
import neopixel
from enum import Enum

class arrow(Enum):

    left = 0

    up = 1

    down = 2

    right = 3

led_per_square = 30

pixels = neopixel.NeoPixel(board.D18, 10 * led_per_square, auto_write=False, pixel_order=neopixel.GRB)

bus = SMBus(1) # indicates /dev/ic2-1
addrs = board.I2C().scan()

port = serial.Serial("/dev/ttyS0", baudrate=115200) # ttyAMA0 for RPi 3

def clear_led():
    pixels.fill((0,0,0))
    pixels.show()

def set_led(index, color):
    for i in range(index * led_per_square, (index+1) * led_per_square):
        pixels[i] = color

def main():
    clear_led()
    while True:
        time.sleep(0.1)
        
        for addr in addrs:
            v = bus.read_i2c_block_data(addr, 0, 16)
            v = struct.unpack('ffff', bytearray(v))
            print(addr, v)

            for i in v:
                if i > 800:    
                    port.write(arrow(i).name)
                    
        for line in port.read():
            line = port.readline()

            color_data = line.split()

            # read color data
            if color_data[1] == 'perfect':
                color = (0, 255, 0)
                pass

            set_led(arrow[color_data[0]].value, color)
            

        pixels.show()

if __name__ == '__main__':
    main()
