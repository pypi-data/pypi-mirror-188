from javonet.core.handler.CommandHandler.AbstractCommandHandler import *
import sys


class LoadLibraryHandler(AbstractCommandHandler):
    loaded_library = 0

    def __init__(self):
        pass

    def process(self, python_command):
        try:
            if len(python_command.payload) != 1:
                raise Exception("LoadLibrary payload parameters mismatch")

            sys.path.append(python_command.payload[0])

            return 0
        except ImportError as importError:
            print("Error loading library: " + python_command.payload)
            return importError
