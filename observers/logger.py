import logging
import sys
from observers.observable import Observer
from DTO.message import Message

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(message)s')

class Logger(Observer):
    def __init__(self) -> None:
        self.notify("Logger: __________________________________")
        self.notify("Logger: Started new Logger session. Hello!")

    def notify(self, msg) -> None:
        if isinstance(msg, Message):
            logging.info(f'{msg.logging_stage}->{msg.location},{msg.topic},{msg.sensor_id},{msg.location},{msg.type},{msg.value}')
        if isinstance(msg, str):
            logging.info(msg)

