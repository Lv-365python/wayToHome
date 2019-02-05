"""This module provides base Daemon class."""

import os
import time
from abc import abstractmethod, ABC

from utils.utils import LOGGER


class Daemon(ABC):
    """Provides basic functionality of daemon."""

    def __init__(self, frequency):
        """Initializes the new Daemon instance."""
        self.is_processed = False
        self.frequency = frequency
        self.pid = None
        self.name = self.__class__.__name__

    def start(self):
        """Executes before Daemon instance starts to process user-defined commands."""
        self.pid = os.getpid()
        message = f'{self.name} was successfully started with process id={self.pid}.'
        LOGGER.info(message)
        self.is_processed = True

    def stop(self):
        """Executes after Daemon instance has finished processing user-defined commands."""
        message = f'{self.name} with process id={self.pid} was successfully stopped.'
        LOGGER.info(message)
        self.is_processed = False

    def run(self):
        """Implements permanent repetition for the execution of certain commands."""
        self.start()
        while self.is_processed:
            self.execute()
            time.sleep(self.frequency)
        self.stop()

    @abstractmethod
    def execute(self):
        """Defines commands for execution."""
