import uuid

from javonet.sdk.core.PythonCommandType import PythonCommandType


class ReferencesCache(object):
    _instance = None
    references_cache = dict()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReferencesCache, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def cache_reference(self, object_reference):
        uuid_ = str(uuid.uuid4())
        self.references_cache[uuid_] = object_reference
        return uuid_

    def resolve_reference(self, python_command):
        if python_command.command_type != PythonCommandType.Reference:
            raise Exception(
                "Trying to dereference Python command with command_type: " + str(python_command.command_type))
        try:
            return self.references_cache[python_command.payload[0]]
        except KeyError:
            raise Exception("Object not found in references")

    def delete_reference(self, reference_guid):
        try:
            del self.references_cache[reference_guid]
            return 0
        except KeyError:
            raise Exception("Object not found in references")
