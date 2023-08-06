from importlib import import_module

from javonet.core.handler.CommandHandler.AbstractCommandHandler import AbstractCommandHandler


class GetTypeHandler(AbstractCommandHandler):
    def __init__(self):
        self._required_parameters_count = 1

    def process(self, python_command):
        try:
            if len(python_command.payload) < self._required_parameters_count:
                raise Exception("GetTypeHandler parameters mismatch!")
            if len(python_command.payload) == 1:
                type_name = python_command.payload[0].split(".")
                if len(type_name) == 1:
                    return import_module(type_name[0])
                else:
                    loaded_module = import_module(".".join(type_name[:-1]))
                    return getattr(loaded_module, type_name[-1])
            else:
                return import_module(".".join(python_command.payload[:]))
        except Exception as e:
            return e
