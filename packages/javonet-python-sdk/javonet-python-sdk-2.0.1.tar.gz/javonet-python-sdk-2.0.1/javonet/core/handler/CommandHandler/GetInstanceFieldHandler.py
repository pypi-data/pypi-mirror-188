from javonet.core.handler.CommandHandler.AbstractCommandHandler import *


class GetInstanceFieldHandler(AbstractCommandHandler):

    def __init__(self):
        self._required_parameters_count = 2

    def process(self, python_command):
        try:
            if len(python_command.payload) != self._required_parameters_count:
                raise Exception("GetInstanceFieldHandler parameters mismatch!")
            clazz = python_command.payload[0]
            value = getattr(clazz, python_command.payload[1])
            return value
        except Exception as e:
            return e

