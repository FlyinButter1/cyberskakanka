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

    up = 0

    left = 1

    down = 2

    right = 3

led_per_square = 60

pixels = neopixel.NeoPixel(board.D21, 4 * led_per_square, auto_write=False, pixel_order=neopixel.GRB)

bus = SMBus(1) # indicates /dev/ic2-1
addrs = board.I2C().scan()

port = serial.Serial("/dev/serial0", baudrate=115200, timeout=0.001) # ttyAMA0 for RPi 3

def clear_led():
    pixels.fill((0,0,0))
    pixels.show()

def set_led(index, color):
    for i in range(index * led_per_square, (index+1) * led_per_square):
        pixels[i] = color

is_pressed = [False, False ,False, False]


def main():
    clear_led()
    while True:
        
        for addr in addrs:
            # podejście na chama 
            # nie wiem czemu działa 😭😭
            while True:
                try:
                    v = bus.read_i2c_block_data(addr, 0, 16)
                    v = struct.unpack('ffff', bytearray(v))
                    break

                except:
                    print("blad")
                    pass

            # print(v)

            for i in range(len(v)):
                if v[i] > 700:
                    if not is_pressed[i]:
                        is_pressed[i] = True
                        port.write(bytes(arrow(i).name, "UTF-8"))
                else:
                    is_pressed[i] = False

        
        for line in  port.readlines():
            line = line.decode()
            color_data = line.split()
            color = (int(color_data[1]), int(color_data[2]), int(color_data[3]))
            set_led(arrow[color_data[0]].value, color)
            pixels.show()



        # for line in port.read():
        #     if line:
        #         line = port.readline()
        #         print(line)
        #         color_data = line.decode().split()
        #         # color_data - tablica z kierunkiem strzalki i rgb

            

        

if __name__ == '__main__':
    main()
