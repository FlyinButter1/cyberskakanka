#  Raspberry Pi Master for Arduino Slave
#  i2c_master_pi.py
#  Connects to Arduino via I2C
  #  DroneBot Workshop 2019
#  https://dronebotworkshop.com

import math
import struct
import time
import board
import neopixel
from smbus2 import SMBus


led_per_square = 59

pixels = neopixel.NeoPixel(board.D21, 4 * led_per_square, auto_write=False, pixel_order=neopixel.GRB)

bus = SMBus(1) # indicates /dev/ic2-1
addrs = board.I2C().scan()

def clear_led():
    pixels.fill((0,0,0))
    pixels.show()

def set_led(index, color):
    for i in range(index * led_per_square, (index+1) * led_per_square):
        pixels[i] = color

def main():
    clear_led()
    
    # set_led(0, (0, 255, 0))
    # set_led(1, (0, 255, 0))
    # set_led(2, (0, 255, 0))
    # set_led(3, (0, 255, 0))

    # pixels.show()

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



            time.sleep(0.1)
            print(v)
        
        for i in range(4):
            if v[i] > 800.0:
                
                set_led(i, (255,0,0))

            else:
                set_led(i, (0,0,0))

            pixels.show()


            

if __name__ == '__main__':
    main()
