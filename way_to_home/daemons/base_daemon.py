"""This module provides base Daemon class."""

import os
import time
from abc import abstractmethod


class Daemon:
    """Provides basic functionality of daemon."""

    def __init__(self, frequency):
        """Initializes the new Daemon instance."""
        self.is_processed = True
        self.frequency = frequency
        self.pid = None
        self.name = self.__class__.__name__

    def start(self):
        """Executes before Daemon instance starts to process user-defined commands."""
        self.pid = os.getpid()
        message = f'{self.name} was successfully started with process id={self.pid}.'
        print(message)

    def stop(self):
        """Executes after Daemon instance has finished processing user-defined commands."""
        message = f'{self.name} with process id={self.pid} was successfully stopped.'
        print(message)

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
