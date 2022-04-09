import board
import neopixel
import time

print('Ready!')
i2c = board.I2C()
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.1

while True:
  i2c.try_lock()
  try:
    print('Writing "30" to address 0x41')
    i2c.writeto(address=0x41, buffer='30')
    led[0] = (0, 0, 255)
  except OSError:
    print('Write failed')
  i2c.unlock()
  time.sleep(5)
  led[0] = 0