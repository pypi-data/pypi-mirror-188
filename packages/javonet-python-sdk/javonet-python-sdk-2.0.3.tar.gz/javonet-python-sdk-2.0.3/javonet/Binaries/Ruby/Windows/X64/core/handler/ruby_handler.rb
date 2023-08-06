require_relative '../../sdk/core/runtime_lib'
require_relative '../../sdk/core/ruby_command_type'
require_relative '../../core/handler/abstract_handler'
require_relative '../../core/handler/command_handler/load_library_handler'
require_relative '../../core/handler/command_handler/invoke_static_method_handler'
require_relative '../../core/handler/command_handler/get_static_field_handler'
require_relative '../../core/handler/command_handler/get_instance_field_handler'
require_relative '../../core/handler/command_handler/create_class_instance_handler'
require_relative '../../core/handler/command_handler/set_static_field_handler'
require_relative '../../core/handler/command_handler/get_type_handler'
require_relative '../../core/handler/command_handler/invoke_instance_method_handler'
require_relative '../../core/handler/command_handler/resolve_instance_handler'
require_relative '../../core/handler/command_handler/casting_handler'
require_relative '../../core/handler/command_handler/destruct_reference_handler'
require_relative '../../core/handler/references_cache'
require_relative '../../core/handler/handler_dictionary'


class RubyHandler < AbstractHandler

  def initialize
    super
    load_library_handler = LoadLibraryHandler.new
    invoke_static_method_handler = InvokeStaticMethodHandler.new
    get_static_field_handler = GetStaticFieldHandler.new
    get_class_instance_handler = CreateClassInstanceHandler.new
    set_static_field_handler = SetStaticFieldHandler.new
    get_type_handler = GetTypeHandler.new
    invoke_instance_method_handler = InvokeInstanceMethodHandler.new
    resolve_instance_handler = ResolveInstanceHandler.new
    casting_handler = CastingHandler.new
    get_instance_field_handler = GetInstanceFieldHandler.new
    destruct_reference_handler = DestructReferenceHandler.new

    $handler_dict[RubyCommandType::LOAD_LIBRARY] = load_library_handler
    $handler_dict[RubyCommandType::INVOKE_STATIC_METHOD] = invoke_static_method_handler
    $handler_dict[RubyCommandType::GET_STATIC_FIELD] = get_static_field_handler
    $handler_dict[RubyCommandType::CREATE_CLASS_INSTANCE] = get_class_instance_handler
    $handler_dict[RubyCommandType::SET_STATIC_FIELD] = set_static_field_handler
    $handler_dict[RubyCommandType::GET_TYPE] = get_type_handler
    $handler_dict[RubyCommandType::INVOKE_INSTANCE_METHOD] = invoke_instance_method_handler
    $handler_dict[RubyCommandType::REFERENCE] = resolve_instance_handler
    $handler_dict[RubyCommandType::CAST] = casting_handler
    $handler_dict[RubyCommandType::GET_INSTANCE_FIELD] = get_instance_field_handler
    $handler_dict[RubyCommandType::DESTRUCT_REFERENCE] = destruct_reference_handler
  end


  def handle_command(ruby_command)
    response = $handler_dict[ruby_command.command_type].handle_command(ruby_command)
    reference_cache = ReferencesCache.instance
      if response.is_a? String or response.is_a? Float or response.is_a? Integer or response.is_a? TrueClass or response.is_a? FalseClass
        return RubyCommand.new(RuntimeLib::RUBY, RubyCommandType::RESPONSE, [response])
      elsif response.is_a? Exception
        return RubyCommand.new(RuntimeLib::RUBY, RubyCommandType::EXCEPTION, ["RubyException: " + response.to_s])
      else
        guid = reference_cache.cache_reference(response)
        return RubyCommand.new(RuntimeLib::RUBY, RubyCommandType::REFERENCE, [guid])
      end
  end
end
