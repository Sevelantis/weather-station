from signals.signal_handler import signal_handler
from DTO.message import Message, LoggingStage
from observers.observable import Observable
from threading import *
import logging
import time as time

class Sensor(Thread, Observable):
    def __init__(self):
        Thread.__init__(self)
        Observable.__init__(self)
     
    def build_message(self, type, value, logging_stage=None) -> Message:
        return Message(topic=self.topic, sensor_id=self.sensor_id, location=self.location, type=type, value=value, logging_stage=logging_stage)

    def read_data(self) -> None:
        sensor_data = self.get_sensor_data()
        time.sleep(3)
        if sensor_data:
            for type, value in sensor_data:
                self.notify_observers(self.build_message(type=type, value=value, logging_stage=LoggingStage.COLLECTED.value))
    
    def run(self) -> None:
        while self.running:
            self.read_data()
            if signal_handler.SIGINT:
                logging.info(f'{self.name}: Exiting thread, SIGINT detected.')
                self.running = False
                break
        logging.info(f"{self.name}: Thread exited.")