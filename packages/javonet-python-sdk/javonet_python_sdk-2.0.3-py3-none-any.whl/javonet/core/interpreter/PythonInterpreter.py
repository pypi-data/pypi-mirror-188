from javonet.core.handler.PythonHandler import PythonHandler
from javonet.core.protocol.CommandDeserializer import CommandDeserializer
from javonet.core.protocol.CommandSerializer import CommandSerializer


class PythonInterpreter:

    def execute(self, python_command, connection_type, tcp_address):
        from javonet.core.transmitter.PythonTransmitter import PythonTransmitter
        command_serializer = CommandSerializer()
        serialized_command = command_serializer.encode(python_command, connection_type, tcp_address)
        serialized_response = PythonTransmitter.send_command(serialized_command)
        command_deserializer = CommandDeserializer(serialized_response, len(serialized_response))
        return command_deserializer.decode()

    def process(self, byte_array, byte_array_len):
        command_deserializer = CommandDeserializer(byte_array, byte_array_len)
        received_command = command_deserializer.decode()
        python_handler = PythonHandler()
        command_serializer = CommandSerializer()
        response_command = python_handler.HandleCommand(received_command)
        encoded_response = command_serializer.encode(response_command, 0, "0.0.0.0:0")
        return encoded_response
