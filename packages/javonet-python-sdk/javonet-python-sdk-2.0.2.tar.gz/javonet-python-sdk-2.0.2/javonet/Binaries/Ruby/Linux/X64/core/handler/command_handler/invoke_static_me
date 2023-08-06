require_relative '../../../sdk/core/runtime_lib'
require_relative '../../../sdk/core/ruby_command_type'
require_relative '../../../sdk/core/ruby_command'
require_relative 'abstract_command_handler'

class InvokeStaticMethodHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 2
  end
  def process(ruby_command)
    return invoke_static_method(ruby_command)
  end

  def invoke_static_method(ruby_command)
    begin
    if ruby_command.payload.length < @required_parameters_count
      raise "Static method parameters mismatch"
    end
    if ruby_command.payload.length > @required_parameters_count
      args = ruby_command.payload[2..]
      ruby_command.payload[0].send(ruby_command.payload[1],*args)
    else
      ruby_command.payload[0].send(ruby_command.payload[1])
    end
    rescue Exception => e
      return e
    end
  end
end
