'''
Magnetometer HMC5883L module. I2C protocol

PINOUT:
    MAG |   RPI
1   VCC |   2 (5.0V)
2   GND |   14 (GND)
3   SCL |   27 (I2C dev 0)
4   SDA |   28 (I2C dev 0)
5   DRDY|   -

'''
from transmitter.sensors.modules.HMC5883L import HMC5883L
from transmitter.sensors.sensor import Sensor
import logging

class Magnetometer(Sensor):
    def __init__(self, HMC_observers):
        Sensor.__init__(self)
        self.name = 'MAG'
        self.running = True
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'
        self.HMC_observers = HMC_observers

    def get_sensor_data(self):
        try:
            (x, y, z) = self.dev.get_axes()
            # heading = self.dev.getHeading()
            if x and y and z:
                return [
                        ('x', x),
                        ('y', y),
                        ('z', z)
                    ]
            else:
                logging.info(f"{self.name}: No data returned.")
        except RuntimeError as error:
            logging.info(f"{self.name}: {error.args[0]}")
        except Exception as error:
            logging.info(f"{self.name}: {error}")

    def run(self):
        # Init Device
        try:
            self.dev = HMC5883L(port=0, observers=self.HMC_observers)
        except Exception as e:
            logging.info(f'{self.name}: Init failed, reason: {e}')
        super().run()
        # close i2c
        if self.dev:
            self.dev.close()
            logging.info(f'{self.name}: I2C device cleaned.')
