from javonet.core.handler.PythonHandler import PythonHandler
from javonet.core.interpreter.PythonInterpreter import PythonInterpreter
from javonet.sdk.core.PythonCommand import PythonCommand
from javonet.sdk.core.PythonCommandType import PythonCommandType
from javonet.sdk.core.RuntimeLib import RuntimeLib
from javonet.sdk.internal.ConnectionType import ConnectionType
from javonet.sdk.internal.abstract.AbstractInstanceContext import AbstractInstanceContext
from javonet.sdk.internal.abstract.AbstractInvocationContext import AbstractInvocationContext
from javonet.sdk.internal.abstract.AbstractMethodInvocationContext import AbstractMethodInvocationContext


class InvocationContext(AbstractInvocationContext, AbstractMethodInvocationContext, AbstractInstanceContext):

    def __init__(self, runtime_lib: RuntimeLib, connection_type: ConnectionType, tcp_ip_address,
                 current_command: PythonCommand, is_executed=False):
        self.__is_executed = is_executed
        self.__runtime_lib = runtime_lib
        self.__connection_type = connection_type
        self.__tcp_ip_address = tcp_ip_address
        self.__current_command = current_command
        self.__response_command = None
        self.__python_interpreter = PythonInterpreter()
        self.__python_handler = None

    def __del__(self):
        if self.__current_command.command_type == PythonCommandType.Reference and self.__is_executed is True:
            self.__current_command = PythonCommand(self.__runtime_lib, PythonCommandType.DestructReference,
                                                   self.__current_command.payload)
            self.execute()

    def execute(self):
        if self.__runtime_lib is RuntimeLib.python:
            self.__python_handler = PythonHandler()
            self.__response_command = self.__python_handler.HandleCommand(self.__current_command)
        else:
            self.__response_command = self.__python_interpreter.execute(self.__current_command,
                                                                        self.__connection_type,
                                                                        self.__tcp_ip_address)

        if self.__response_command.command_type == PythonCommandType.Exception:
            raise Exception(self.__response_command.payload[0])

        if self.__current_command.command_type == PythonCommandType.CreateClassInstance:
            self.__current_command = self.__response_command
            self.__is_executed = True
            return self

        return InvocationContext(self.__runtime_lib, self.__connection_type, self.__tcp_ip_address,
                                 self.__response_command, True)

    def invoke_static_method(self, *args):
        local_command = PythonCommand(self.__runtime_lib, PythonCommandType.InvokeStaticMethod, [*args])
        return InvocationContext(self.__runtime_lib, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def invoke_instance_method(self, *args):
        local_command = PythonCommand(self.__runtime_lib, PythonCommandType.InvokeInstanceMethod, [*args])
        return InvocationContext(self.__runtime_lib, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def get_static_field(self, *args):
        local_command = PythonCommand(self.__runtime_lib, PythonCommandType.GetStaticField, [*args])
        return InvocationContext(self.__runtime_lib, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def set_static_field(self, *args):
        local_command = PythonCommand(self.__runtime_lib, PythonCommandType.SetStaticField, [*args])
        return InvocationContext(self.__runtime_lib, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def create_instance(self, *args):
        local_command = PythonCommand(self.__runtime_lib, PythonCommandType.CreateClassInstance, [*args])
        return InvocationContext(self.__runtime_lib, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def set_generic_type(self, string: str):
        return self

    def get_instance_field(self, *args):
        local_command = PythonCommand(self.__runtime_lib, PythonCommandType.GetInstanceField, [*args])
        return InvocationContext(self.__runtime_lib, self.__connection_type, self.__tcp_ip_address,
                                 self.__build_command(local_command))

    def get_value(self):
        return self.__current_command.payload[0]

    def __build_command(self, command):
        for i in range(len(command.payload)):
            if isinstance(command.payload[i], InvocationContext):
                command.payload[i] = command.payload[i].__current_command

        if self.__current_command is None:
            return command
        else:
            return command.add_arg_to_payload_on_beginning(self.__current_command)
