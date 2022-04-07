""" The main module """
import math
from time import time
import json
import server

# A dict of route shortnames to route ids
#__ROUTES = {'38': '20038', 'R29': '10029', 'B43': '30043', 'B43E': '30943'}

def departure_info(directions):
  """ Gets the InternetServiceDesc and time until departure data for each route """
  unique_isds = []
  for direction in directions:
    for departure in direction['Departures']:
      trip = departure['Trip']
      # SDT ex: /Date(1648627309163-0400)\, where 1648627309163 is ms since the epoch.
      # We don't care about the time zone (plus it's wrong), so we just want the seconds. We strip
      # off the leading '/Date(' and trailing '-400)\' + the last 3 digits to do a rough conversion to seconds.
      sdt = math.ceil(int(departure['SDT'][6:-10]))
      isd = trip['InternetServiceDesc']
      # If there is a departure with a unique ISD, and it's in the future, and it's not skipped
      if (isd not in unique_isds) and (sdt > time()) and (departure['StopStatusReportLabel'] != 'Skipped'):
        unique_isds.append(isd)
        # Avail's time feed seems to be off by 4 minuets
        time_diff = (sdt - time()) / 60
        send_departure_time(isd, math.floor(time_diff))

def send_departure_time(isd, time_diff):
  """ Sends the InternetServiceDesc and time until departure data down the I2C bus """
  print(isd, time_diff)

http_response = server.get_stopdepartures()

# The json response is in an array, since we're only requesting one item we can manually remove
# the square brackets before parsing the bytestring to stop the parser from thinking it's a list
response = json.loads(http_response[1:-1])

departure_info(response['RouteDirections'])