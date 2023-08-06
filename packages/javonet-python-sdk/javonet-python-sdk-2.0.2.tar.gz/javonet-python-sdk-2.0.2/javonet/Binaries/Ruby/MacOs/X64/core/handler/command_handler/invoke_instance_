require_relative '../../../sdk/core/runtime_lib'
require_relative '../../../sdk/core/ruby_command_type'
require_relative '../../../sdk/core/ruby_command'
require_relative 'abstract_command_handler'


class InvokeInstanceMethodHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 2
  end
  def process(ruby_command)
    return invoke_instance_method(ruby_command)
  end

  def invoke_instance_method(ruby_command)
    begin
    if ruby_command.payload.length < @required_parameters_count
      raise "InvokeInstanceMethod parameters mismatch"
    end
    if ruby_command.payload.length > 2
      arguments = ruby_command.payload[2..]
      return ruby_command.payload[0].send(ruby_command.payload[1], *arguments)
    else
      return ruby_command.payload[0].send(ruby_command.payload[1])
    end
    rescue Exception => e
      return e
    end
  end
end