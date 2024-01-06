import threading
import time
import Adafruit_DHT
from application.app import db
from application.models import Temp
from datetime import datetime

class TempMonitorThread(threading.Thread):

     def run(self):
          print("Monitor system thread")

          try:
               while 1: # Monitor the system forever while powered
                    latest_temp = Temp.query.order_by(Temp.measure_datetime.desc()).first()
                    if not latest_temp or not latest_temp.measure_datetime or (latest_temp.measure_datetime - datetime.utcnow()).seconds > 3600:
                         print('Executing temp measurement daemon.')

                         humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 2) #discard first reading cuz inaccurate
                         time.sleep(3)

                         humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 2)
                         t = Temp(temp=round(temperature, 2), measure_datetime=datetime.utcnow())

                         db.session.add(t)
                         db.session.commit()

                         time.sleep(3597)
                    else:
                         time.sleep(3600 - (latest_temp.measure_datetime - datetime.utcnow()).seconds)
          except KeyboardInterrupt:
               GPIO.cleanup()
