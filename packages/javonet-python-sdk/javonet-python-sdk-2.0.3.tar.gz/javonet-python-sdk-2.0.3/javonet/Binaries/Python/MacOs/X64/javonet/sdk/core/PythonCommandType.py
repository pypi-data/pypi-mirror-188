from enum import Enum


class PythonCommandType(Enum):
    Response = 0
    LoadLibrary = 1
    InvokeStaticMethod = 2
    GetStaticField = 3
    SetStaticField = 4
    CreateClassInstance = 5
    GetType = 6
    Reference = 7
    GetModule = 8
    InvokeInstanceMethod = 9
    Exception = 10
    HeartBeat = 11
    Cast = 12
    GetInstanceField = 13
    Optimize = 14
    GenerateLib = 15
    InvokeGlobalMethod = 16
    DestructReference = 17
