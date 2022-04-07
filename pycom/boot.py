import gc
from time import sleep_ms
from machine import RTC, I2C
from network import WLAN
import pycom

wlan = WLAN()
rtc = RTC()
# create on bus 0
i2c = I2C(0)
i2c.init(I2C.MASTER, baudrate=400000)

# Turn off the LED
pycom.heartbeat(False)

# Garbage collect incase old ssl sockets persisted
gc.collect()

if not wlan.isconnected():
  wlan.connect(ssid = 'Abraham Linksys', auth = (WLAN.WPA2, 'grandcarrot572'))
  print('connecting..', end = '')
  i = 0
  while not wlan.isconnected():
    sleep_ms(250)
    print('.', end = '')
    if i == 20:
      machine.reset()
    else:
      i = i + 1
  print('connected')

# Inits the RTC and sets up automatic fetch and update the time using NTP
rtc.ntp_sync('pool.ntp.org')
# Wait for ntp to sync before adjusting timezon
sleep_ms(750)