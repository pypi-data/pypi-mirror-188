class PythonCommand:
    target_runtime = None
    command_type = None
    payload = []

    def __init__(self, targetRuntime, commandType, payload):
        self.target_runtime = targetRuntime
        self.command_type = commandType
        self.payload = payload

    def to_string(self):
        return 'Target runtime: ' + str(self.target_runtime) + ' Command type: ' + str(
            self.command_type) + ' Payload: ' + str(self.payload)

    def get_payload(self):
        return self.payload

    def __eq__(self, element):
        self.is_equal = False
        if self is element:
            self.is_equal = True
        if element is None or self.__class__ != element.__class__:
            self.is_equal = False
        if self.command_type is element.command_type and self.target_runtime is element.target_runtime:
            self.is_equal = True
        if len(self.payload) == len(element.payload):
            i = 0
            array_item_equal = False
            for payload_item in self.payload:
                if payload_item.__eq__(element.payload[i]):
                    array_item_equal = True
                else:
                    array_item_equal = False
                i += 1
            self.is_equal = array_item_equal
        else:
            self.is_equal = False
        return self.is_equal

    def set_payload(self, payload_item):
        self.payload.append(payload_item)

    def add_arg_to_payload(self, argument):
        merged_payload = self.payload + [argument]
        return PythonCommand(self.target_runtime, self.command_type, merged_payload)

    def append_payload(self, argument):
        self.payload.append([argument])

    def add_arg_to_payload_on_beginning(self, argument):
        merged_payload = [argument] + self.payload
        return PythonCommand(self.target_runtime, self.command_type, merged_payload)

    def drop_first_payload_argument(self):
        payload_args = []
        payload_args.extend(self.payload)
        if len(payload_args) != 0:
            payload_args.pop(0)
        return PythonCommand(self.target_runtime, self.command_type, payload_args)
