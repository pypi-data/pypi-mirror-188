require_relative 'abstract/abstract_runtime_context'
require_relative 'invocation_context'
require_relative 'connection_type'
require_relative '../../core/interpreter/ruby_interpreter'

class RuntimeContext < AbstractRuntimeContext

  @@memory_runtime_contexts = Hash.new
  @@network_runtime_contexts = Hash.new

  def initialize
    @current_command = 0
    @ruby_interpreter = nil
    @ruby_handler = nil
  end

  def self.get_instance(runtime_lib, connection_type, tcp_address)
    if (ConnectionType::TCP == connection_type) && tcp_address == nil
      if @@network_runtime_contexts.has_key?(tcp_address)
        runtime_ctx = @@network_runtime_contexts[tcp_address]
        runtime_ctx.current_command = 0
        return runtime_ctx
      else
        runtime_ctx = RuntimeContext.new(runtime_lib, connection_type, tcp_address)
        @@network_runtime_contexts[:tcp_address] = runtime_ctx
        return runtime_ctx
      end
    else
      if (@@memory_runtime_contexts.has_key?(runtime_lib))
        runtime_ctx = @@network_runtime_contexts[runtime_lib]
        runtime_ctx.current_command = 0
        return runtime_ctx
      else
        runtime_ctx = RuntimeContext.new(runtime_lib, connection_type, nil)
        @@memory_runtime_contexts[:tcp_address] = runtime_ctx
        return runtime_ctx
      end
    end
  end

  def initialize(runtime_lib, connection_type, tcp_address)
    @runtime_lib = runtime_lib
    @connection_type = connection_type
    @tcp_ip_address = tcp_address
  end

  def execute(command)
    if @runtime_lib == RuntimeLib::RUBY
      @ruby_handler = RubyHandler.new
      @ruby_handler.handle_command(command)
    else
      @ruby_interpreter = RubyInterpreter.new
      @ruby_interpreter.execute(command, @connection_type, @tcp_ip_address)
    end
  end

  def current_command
    return @current_command
  end

  def load_library(*constructor_args)
    local_command = RubyCommand.new(@runtime_lib, RubyCommandType::LOAD_LIBRARY, [*constructor_args])
    self.execute(local_command)
    return self
  end

  def get_type(*constructor_args)
    local_command = RubyCommand.new(@runtime_lib, RubyCommandType::GET_TYPE, [*constructor_args])
    return InvocationContext.new(@runtime_lib, @connection_type, @tcp_ip_address, build_command(local_command), false)
  end

  def build_command(command)
    if @current_command.nil?
      return command
    else
      return command.add_arg_to_payload_on_beginning(@current_command)
    end
  end

end