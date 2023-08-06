from javonet.sdk.core.PythonCommand import PythonCommand
from javonet.sdk.core.PythonCommandType import PythonCommandType


class ExplicitCast:
    @staticmethod
    def cast(value, target_type):
        return PythonCommand(
            100,
            PythonCommandType.Cast,
            [
                value,
                PythonCommand(
                    100,
                    PythonCommandType.GetType,
                    [
                        target_type
                    ]
                )
            ]
        )
