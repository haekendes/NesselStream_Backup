from flask import render_template, Response, request, send_file
from application.app import app, db
import RPi.GPIO as GPIO
import time
from datetime import datetime
from importlib import import_module
import Adafruit_DHT
from picamera import PiCamera
from config import Config
from application.models import Temp
from PIL import Image
import io
import sys


@app.get('/')
def home():
    return render_template('home.html', title='Haekendes Nessel Stream - Redux')


@app.route('/temp')
def temp():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 2)
    if temperature:
        #return {'temp': 'Temperatur: {0:0.1f}°C, Feuchtigkeit: {1:0.1f}%'.format(temperature, humidity) }
        return {'temp': 'Temperatur: {0:0.1f}°C'.format(temperature) }
    else:
        return {'temp': 'Lesen des Temperatursensors fehlgeschlagen.'}


@app.route('/temps')
def temps():
    temp_list = [x for x in Temp.query.all()]
    return {'temps': temp_list}


@app.route('/giessen', methods=['POST'])
def giessen():
    safetyPin = request.args.get('safetyPin', None)
    timeValue = request.args.get('timeRange', None)

    float_value = float(timeValue)
    
    if safetyPin == '0667':
        if 0 < float_value <= 5:
            GPIO.output(23, GPIO.HIGH)
            time.sleep(float_value)
            GPIO.output(23, GPIO.LOW)
        else:
            GPIO.output(23, GPIO.LOW)
            return {'time': datetime.now().strftime("%d.%m.%Y %H:%M:%S"), 'result': 'Schwerwiegender Fehler, val: ' + timeValue}, 500
        return {'time': datetime.now().strftime("%d.%m.%Y %H:%M:%S"), 'result': timeValue + ' Sekunden gegossen'}, 200
    else:
        time.sleep(float_value)
        return {'time': datetime.now().strftime("%d.%m.%Y %H:%M:%S"), 'result': timeValue + ' Sekunden gegossen :)'}, 200


@app.route('/picture')
def picture():
    #try:
        #camera = PiCamera()
        #image_path = f'{Config.basedir}/application/static/image.jpg'
        #camera.capture(image_path)
    #except Exception:
        #print('Exception in picture route.')
    #finally:
        #camera.close()

    stream = io.BytesIO()
    with PiCamera() as camera:
        camera.capture(stream, format='jpeg')
        stream.seek(0) # "Rewind" the stream to the beginning so we can read its content

    compressed_stream = io.BytesIO() # new stream, otherwise both images end up in the original stream, almost doubling image size
    with Image.open(stream) as image:
        #foo = Image.open(image_path)
        image.save(compressed_stream, format='JPEG', optimize=True, quality=85)
        compressed_stream.seek(0)

    #return send_file(image_path)
    return send_file(
                     compressed_stream,
                     attachment_filename='image.jpeg',
                     mimetype='image/jpg'
               )
