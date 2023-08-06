from javonet.core.generator.handler.AbstractGeneretatorHandler import AbstractGeneratorHandler
from javonet.core.generator.internal.SharedHandlerType import SharedHandlerType
from javonet.sdk.core.PythonCommand import PythonCommand
from javonet.sdk.core.PythonCommandType import PythonCommandType
from javonet.sdk.core.RuntimeLib import RuntimeLib


class GetStaticFieldGeneratorHandler(AbstractGeneratorHandler):

    def generate_command(self, analyzed_object, parent_command, handlers):
        get_static_field_command = PythonCommand(RuntimeLib.python, PythonCommandType.GetStaticField, [])
        get_static_field_command = get_static_field_command.add_arg_to_payload(
            handlers.SHARED_HANDLER[SharedHandlerType.METHOD_NAME].generate_command(analyzed_object[0],
                                                                                    get_static_field_command, handlers))
        get_static_field_command = get_static_field_command.add_arg_to_payload(
            handlers.SHARED_HANDLER[SharedHandlerType.TYPE].generate_command(analyzed_object[1],
                                                                             get_static_field_command,
                                                                             handlers))
        get_static_field_command = get_static_field_command.add_arg_to_payload(
            handlers.SHARED_HANDLER[SharedHandlerType.MODIFIER].generate_command(analyzed_object,
                                                                                 get_static_field_command,
                                                                                 handlers))
        get_static_field_command = get_static_field_command.add_arg_to_payload(
            handlers.SHARED_HANDLER[SharedHandlerType.CLASS_NAME].generate_command(parent_command.get_payload()[0],
                                                                                   get_static_field_command,
                                                                                   handlers))
        return get_static_field_command

    def generate_code(self, existing_string_builder, common_command, used_object, handlers):
        existing_string_builder.append("    ")
        handlers.SHARED_HANDLER[SharedHandlerType.MODIFIER].generate_code(existing_string_builder, common_command,
                                                                          used_object.get_payload()[2], handlers)

        handlers.SHARED_HANDLER[SharedHandlerType.METHOD_NAME].generate_code(existing_string_builder, common_command,
                                                                             used_object.get_payload()[0], handlers)
        existing_string_builder.append(" = ")
        handlers.SHARED_BODY_HANDLER[PythonCommandType.GetStaticField].generate_code(existing_string_builder,
                                                                                     common_command,
                                                                                     used_object, handlers)
