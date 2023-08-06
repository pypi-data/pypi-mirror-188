from javonet.core.interpreter.PythonInterpreter import PythonInterpreter


class Receiver:

    def __init__(self):
        self.python_interpreter = PythonInterpreter()

    def SendCommand(self, messageByteArray, messageByteArrayLen):
        return bytearray(self.python_interpreter.process(messageByteArray, len(messageByteArray)))

    def HeartBeat(self, messageByteArray, messageByteArrayLen):
        return bytearray([49, 48])
