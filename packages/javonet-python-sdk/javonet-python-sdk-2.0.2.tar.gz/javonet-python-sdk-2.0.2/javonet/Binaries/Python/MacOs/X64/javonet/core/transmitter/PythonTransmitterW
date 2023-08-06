import os
import platform
from ctypes import *

from javonet.core.callback.callbackFunc import callbackFunc

CMPFUNC = CFUNCTYPE(py_object, POINTER(c_ubyte), c_int)
callbackFunction = CMPFUNC(callbackFunc)


class PythonTransmitterWrapper:
    if platform.system() == 'Windows':
        file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        python_lib_path = file_path + '\\Binaries\\Native\\Windows\\X64\\JavonetPythonRuntimeNative.dll'
    if platform.system() == 'Linux':
        file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        python_lib_path = file_path + '/Binaries/Native/Linux/X64/libJavonetPythonRuntimeNative.so'
    if platform.system() == 'Darwin':
        file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        python_lib_path = file_path + '/Binaries/Native/MacOs/X64/libJavonetPythonRuntimeNative.dylib'

    python_lib = cdll.LoadLibrary(python_lib_path)
    python_lib.SetCallback(callbackFunction)

    @staticmethod
    def send_command(message):
        message_array = bytearray(message)
        message_ubyte_array = c_ubyte * len(message_array)
        response_array_len = PythonTransmitterWrapper.python_lib.SendCommand(
            message_ubyte_array.from_buffer(message_array),
            len(message_array))
        if response_array_len > 0:
            response = bytearray(response_array_len)
            response_ubyte_array = c_ubyte * response_array_len
            PythonTransmitterWrapper.python_lib.ReadResponse(response_ubyte_array.from_buffer(response),
                                                             response_array_len)
            return response
        else:
            raise RuntimeError("Javonet native code error: " + str(response_array_len))

    @staticmethod
    def activate(email, licence_key, proxy_host, proxy_user_name, proxy_user_password):
        activate = PythonTransmitterWrapper.python_lib.Activate
        activate.restype = c_int
        activate.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]

        return activate(email.encode('ascii'),
                        licence_key.encode('ascii'),
                        proxy_host.encode('ascii'),
                        proxy_user_name.encode('ascii'),
                        proxy_user_password.encode('ascii'))
