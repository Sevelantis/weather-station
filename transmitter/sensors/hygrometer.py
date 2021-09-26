'''
DHT11 hygrometer & thermometer module.

PINOUT:
    DHT | RPI
1   VCC | 2 (5.0V)
2   SIG | 16 (GPIO) (BCM 23)
3   -   | - 
4   GND | 9 (GND)

Inserted 10K Ohm pull-up resistor binding together VCC and SIG.
'''
import logging
import board
import adafruit_dht
import RPi.GPIO as GPIO
from transmitter.sensors.sensor import Sensor

class Hygrometer(Sensor):
    def __init__(self):
        Sensor.__init__(self)
        self.name = 'HYG'
        self.running = True
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'

    def get_sensor_data(self):
        try:
            temperature = self.dev.temperature
            humidity = self.dev.humidity
            if temperature and humidity:
                return [
                    ('temperature', temperature),
                    ('humidity', humidity)
                ]
            else:
                logging.info(f"{self.name}: No data returned.")
        except RuntimeError as error:
            logging.info(f"{self.name}: {error.args[0]}")
        except Exception as error:
            self.dev.exit()
            logging.info(f"{self.name}: {error}")
            raise error

    def run(self) -> None:
        # Init Device
        try:
            self.dev = adafruit_dht.DHT11(board.D23)
        except Exception as e:
            logging.info(f'{self.name}: Init failed, reason: {e}')
        
        super().run()
        if self.dev:
            self.dev.exit()
            logging.info(f'{self.name}: PulseIO cleaned.')
