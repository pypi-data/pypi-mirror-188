require_relative 'abstract/abstract_invocation_context'
require_relative '../../core/interpreter/ruby_interpreter'

class InvocationContext < AbstractInvocationContext
  def initialize(runtime_lib, connection_type, tcp_ip_address, command, is_executed = false)
    @is_executed = is_executed
    @runtime_lib = runtime_lib
    @connection_type = connection_type
    @tcp_ip_address = tcp_ip_address
    @current_command = command
    @response_command = nil
    @ruby_interpreter = nil
    @ruby_handler = nil
    ObjectSpace.define_finalizer(self, self.finalize(@current_command, @is_executed, @ruby_interpreter, @connection_type, @tcp_ip_address))
  end

  def finalize(command, is_executed, ruby_interpreter, connection_type, tcp_ip_address)
    proc do
      if command.command_type == RubyCommandType::REFERENCE && is_executed == true
        destructCommand = RubyCommand.new(@runtime_lib, RubyCommandType::DESTRUCT_REFERENCE, command.payload)
        if @runtime_lib == RuntimeLib::RUBY
          ruby_handler = RubyHandler.new
          ruby_handler.handle_command(destructCommand)
        else
          ruby_interpreter.execute(destructCommand, connection_type, tcp_ip_address)
        end
      end
    end
  end

  def execute
    if @runtime_lib == RuntimeLib::RUBY
      @ruby_handler = RubyHandler.new
      @response_command = @ruby_handler.handle_command(@current_command)
    else
      @ruby_interpreter = RubyInterpreter.new
      @response_command = @ruby_interpreter.execute(@current_command, @connection_type, @tcp_ip_address)
    end

    if @response_command.command_type == RubyCommandType::EXCEPTION
      raise @response_command.payload[0]
    end

    if @response_command.command_type == RubyCommandType::CREATE_CLASS_INSTANCE
      @current_command = @response_command
      @is_executed = true
      return self
    end

    return InvocationContext.new(@runtime_lib, @connection_type, @tcp_ip_address, @response_command, true)
  end

  def get_value
    return @current_command.payload[0]
  end

  def invoke_instance_method(*constructor_args)
    local_command = RubyCommand.new(@runtime_lib, RubyCommandType::INVOKE_INSTANCE_METHOD, [*constructor_args])
    return InvocationContext.new(@runtime_lib, @connection_type, @tcp_ip_address, build_command(local_command))
  end

  def create_instance(*constructor_args)
    local_command = RubyCommand.new(@runtime_lib, RubyCommandType::CREATE_CLASS_INSTANCE, [*constructor_args])
    return InvocationContext.new(@runtime_lib, @connection_type, @tcp_ip_address, build_command(local_command))
  end

  def get_static_field(*constructor_args)
    local_command = RubyCommand.new(@runtime_lib, RubyCommandType::GET_STATIC_FIELD, [*constructor_args])
    return InvocationContext.new(@runtime_lib, @connection_type, @tcp_ip_address, build_command(local_command))
  end

  def set_static_field(*constructor_args)
    local_command = RubyCommand.new(@runtime_lib, RubyCommandType::SET_STATIC_FIELD, [*constructor_args])
    return InvocationContext.new(@runtime_lib, @connection_type, @tcp_ip_address, build_command(local_command))
  end

  def get_instance_field(*constructor_args)
    local_command = RubyCommand.new(@runtime_lib, RubyCommandType::GET_INSTANCE_FIELD, [*constructor_args])
    return InvocationContext.new(@runtime_lib, @connection_type, @tcp_ip_address, build_command(local_command))
  end

  def invoke_static_method(*constructor_args)
    local_command = RubyCommand.new(@runtime_lib, RubyCommandType::INVOKE_STATIC_METHOD, [*constructor_args])
    return InvocationContext.new(@runtime_lib, @connection_type, @tcp_ip_address, build_command(local_command))
  end

  def build_command(command)
    (0..command.payload.length).step(1) do |i|
      if command.payload[i].is_a? InvocationContext
        command.payload[i] = (command.payload[i]).current_command
      end
    end

    if @current_command.nil?
      return command
    else
      return command.add_arg_to_payload_on_beginning(@current_command)
    end
  end

  def current_command
    @current_command
  end

end