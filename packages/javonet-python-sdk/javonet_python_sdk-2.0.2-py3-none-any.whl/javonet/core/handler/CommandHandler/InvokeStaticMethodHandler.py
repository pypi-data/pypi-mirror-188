from javonet.core.handler.CommandHandler.AbstractCommandHandler import *


class InvokeStaticMethodHandler(AbstractCommandHandler):

    def __init__(self):
        self._required_parameters_count = 2

    def process(self, python_command):
        try:
            if len(python_command.payload) < self._required_parameters_count:
                raise Exception("InvokeStaticMethod Parameters mismatch!")

            clazz = python_command.payload[0]
            method = getattr(clazz, python_command.payload[1])

            if len(python_command.payload) > 2:
                method_arguments = python_command.payload[2:]
                return method(*method_arguments)
            return method()
        except Exception as e:
            return e
