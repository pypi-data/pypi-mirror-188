from javonet.core.handler.CommandHandler.AbstractCommandHandler import *


class SetStaticFieldHandler(AbstractCommandHandler):

    def __init__(self):
        self._required_parameters_count = 3

    def process(self, python_command):
        try:
            if len(python_command.payload) != self._required_parameters_count:
                raise Exception("SetStaticFieldHandler parameters mismatch!")

            clazz = python_command.payload[0]
            setattr(clazz, python_command.payload[1], python_command.payload[2])
            return "SetStaticFieldHandler - success"
        except Exception as e:
            return e
