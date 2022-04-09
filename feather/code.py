from adafruit_display_text import label
import board
import displayio
import framebufferio
from i2cperipheral import I2CPeripheral
import neopixel
import rgbmatrix
import terminalio
import time

print('Ready!')
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.1
regs = [0] * 16
index = 0

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
  width = 64, height = 32, bit_depth = 2,
  rgb_pins = [board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
  addr_pins = [board.A5, board.A4, board.A3, board.A2],
  clock_pin = board.D13, latch_pin = board.D0, output_enable_pin = board.D1
)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh = False)

def display_text(text):
  """ Displays the given text on an RBG matrix """

  line = label.Label(
    terminalio.FONT,
    scale = 3,
    color = (255, 0, 120), # These panels are RBG
    text = text
  )
  # Set the text position on the display
  line.x = 15
  line.y = 13

  group = displayio.Group()
  group.append(line)
  display.show(group)
  display.refresh()

with I2CPeripheral(board.SCL, board.SDA, (0x40, 0x41)) as device:
  while True:
    request = device.request()
    if not request:
      # Maybe do some housekeeping
      continue
    # Closes the transfer if necessary by sending a NACK or feeding dummy bytes
    with request:
      # led[0] = (0, 0, 255)
      # if r.address == 0x40:
      #   if not r.is_read:  # Main write which is Selected read
      #     print('read 0x40')
      #     b = r.read(1)
      #     if not b or b[0] > 15:
      #       break
      #     index = b[0]
      #     if b:
      #       regs[index] = b[0]
      #   elif r.is_restart:  # Combined transfer: This is the Main read message
      #     n = r.write(bytes([regs[index]]))
      if request.address == 0x41:
        if not request.is_read:
          led[0] = (0, 255, 0)
          buffer = request.read()
          print(bytearray.decode(buffer))
          #display_text(bytearray.decode(buffer))
    led[0] = 0
