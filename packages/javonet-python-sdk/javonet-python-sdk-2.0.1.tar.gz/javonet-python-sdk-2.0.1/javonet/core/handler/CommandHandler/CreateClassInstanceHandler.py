from inspect import signature

from javonet.core.handler.CommandHandler.AbstractCommandHandler import *


class CreateClassInstanceHandler(AbstractCommandHandler):
    def __init__(self):
        self._required_parameters_count = 1

    def process(self, python_command):
        try:

            if len(python_command.payload) < self._required_parameters_count:
                raise Exception("CreateClassInstanceHandler parameters mismatch!")
            clazz = python_command.payload[0]
            if len(python_command.payload) > 1:
                method_arguments = python_command.payload[1:]
                sig = signature(clazz)
                if len(sig.parameters) != len(method_arguments):
                    raise Exception("Number of arguments for create class instance are not matching!")
                return clazz(*method_arguments)
            return clazz()
        except Exception as e:
            return e
