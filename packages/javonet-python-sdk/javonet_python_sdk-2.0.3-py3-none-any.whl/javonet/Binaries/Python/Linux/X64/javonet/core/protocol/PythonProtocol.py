from javonet.sdk.core import PythonCommand
from javonet.sdk.core import PythonCommandType
from javonet.sdk.core import RuntimeLib


class PythonProtocol:

    @staticmethod
    def serialize(python_command):
        ARGUMENT_SEPARATOR = bytearray(3)
        byte_array_runtime = bytearray([python_command.target_runtime.value])
        byte_array_command = bytearray([python_command.command_type.value])

        payload_array = PythonProtocol.convertToBytes(python_command.payload)

        byte_array = byte_array_runtime + ARGUMENT_SEPARATOR + byte_array_command + ARGUMENT_SEPARATOR + payload_array
        return list(byte_array)

    @staticmethod
    def deserialize(byte_array_list):
        byte_array = bytearray(byte_array_list)
        ARGUMENT_SEPARATOR = bytearray(3)
        byte_array_payload = list()

        x = byte_array.split(ARGUMENT_SEPARATOR)
        byte_array_runtime = RuntimeLib(int.from_bytes(x[0], 'big'))
        byte_array_command = PythonCommandType(int.from_bytes(x[1], 'big'))
        for i in range(2, len(x)):
            byte_array_payload.append(x[i].decode('ascii'))

        return PythonCommand(byte_array_runtime, byte_array_command, byte_array_payload)

    @staticmethod
    def convertToBytes(strings):
        payload_array = bytearray()
        ARGUMENT_SEPARATOR = bytearray(3)
        for i in range(0, len(strings)):
            payload_array += bytearray(strings[i], 'ascii')
            if i != len(strings) - 1:
                payload_array += ARGUMENT_SEPARATOR
        return payload_array

    @staticmethod
    def byteArray2dSize(byteArray):
        ARGUMENT_SEPARATOR = bytearray(3)
        byteArray2dSize = 0
        for i in range(0, len(byteArray)):
            if i != len(byteArray) - 1:
                byteArray2dSize += len(byteArray[i]) + ARGUMENT_SEPARATOR.__sizeof__()
            else:
                byteArray2dSize += len(byteArray[i])
        return byteArray2dSize
