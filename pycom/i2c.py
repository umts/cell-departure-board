from machine import I2C
import pycom
import gc

print(pycom.nvs_get('0'))
for x in range(100000, 500000, 10):
  gc.collect()
  i2c = I2C(0, pins=('P22','P23'))
  i2c.init(I2C.MASTER, baudrate=(x))
  try:
    addr = i2c.writeto(addr=0x41, buf=b'hello')
    # addr[0]
    print('Address:', addr, end='')
    print(' baud rate:', x)
    pycom.nvs_set('0', x)
    pycom.rgbled(0xff00)
    break
  # except IndexError:
  except OSError:
    pycom.rgbled(0xff0000)
    pycom.heartbeat(False)
  i2c.deinit()
  print('\r', x, '/500000', end='')

print('done')