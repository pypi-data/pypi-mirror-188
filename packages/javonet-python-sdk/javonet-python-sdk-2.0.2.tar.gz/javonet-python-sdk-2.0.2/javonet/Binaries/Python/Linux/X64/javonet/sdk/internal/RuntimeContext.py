from javonet.core.handler.PythonHandler import PythonHandler
from javonet.core.interpreter.PythonInterpreter import PythonInterpreter
from javonet.sdk.core.PythonCommand import PythonCommand
from javonet.sdk.core.PythonCommandType import PythonCommandType

from javonet.sdk.core.RuntimeLib import RuntimeLib
from javonet.sdk.internal.ConnectionType import ConnectionType
from javonet.sdk.internal.InvocationContext import InvocationContext
from javonet.sdk.internal.abstract.AbstractTypeContext import AbstractTypeContext


class RuntimeContext(AbstractTypeContext):
    __python_interpreter = PythonInterpreter()
    __python_handler = PythonHandler()
    __memory_runtime_contexts = dict()
    __network_runtime_contexts = dict()
    current_command = None

    @staticmethod
    def get_instance(runtime_lib: RuntimeLib, connection_type: ConnectionType, tcp_address: str):
        if connection_type == ConnectionType.Tcp and tcp_address is not None:
            if tcp_address in RuntimeContext.__network_runtime_contexts:
                runtime_ctx = RuntimeContext.__network_runtime_contexts.get(tcp_address)
                runtime_ctx.current_command = None
                return runtime_ctx
            else:
                runtime_ctx = RuntimeContext(runtime_lib, connection_type, tcp_address)
                RuntimeContext.__network_runtime_contexts[tcp_address] = runtime_ctx
                return runtime_ctx
        else:
            if runtime_lib in RuntimeContext.__memory_runtime_contexts:
                runtime_ctx = RuntimeContext.__memory_runtime_contexts.get(runtime_lib)
                runtime_ctx.current_command = None
                return runtime_ctx
            else:
                runtime_ctx = RuntimeContext(runtime_lib, connection_type, None)
                RuntimeContext.__memory_runtime_contexts[runtime_lib] = runtime_ctx
                return runtime_ctx

    def __init__(self, runtime_lib: RuntimeLib, connection_type: ConnectionType, tcp_address: str):
        self.__isExecuted = False
        self.__runtime_lib = runtime_lib
        self.__connection_type = connection_type
        self.__tcp_ip_address = tcp_address

    def execute(self, command: PythonCommand):
        if self.__runtime_lib is RuntimeLib.python:
            RuntimeContext.__python_handler.HandleCommand(command)
            self.__isExecuted = True
        else:
            RuntimeContext.__python_interpreter.execute(command, self.__connection_type, self.__tcp_ip_address)
            self.__isExecuted = True

    def load_library(self, *args):
        local_command = PythonCommand(self.__runtime_lib, PythonCommandType.LoadLibrary, [*args])
        self.execute(local_command)
        return self

    def get_type(self, *args):
        local_command = PythonCommand(self.__runtime_lib, PythonCommandType.GetType, [*args])
        self.build_command(local_command)
        return InvocationContext(self.__runtime_lib, self.__connection_type, self.__tcp_ip_address,
                                 self.current_command)

    def build_command(self, command):
        if self.current_command is None:
            self.current_command = command
        else:
            self.current_command = command.add_arg_to_payload_on_beginning(self.current_command)
