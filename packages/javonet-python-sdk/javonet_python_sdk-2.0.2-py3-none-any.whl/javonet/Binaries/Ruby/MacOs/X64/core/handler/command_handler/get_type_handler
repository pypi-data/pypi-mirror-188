require_relative '../../../sdk/core/runtime_lib'
require_relative '../../../sdk/core/ruby_command_type'
require_relative '../../../sdk/core/ruby_command'
require_relative 'abstract_command_handler'

class GetTypeHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 1
  end
  def process(ruby_command)
    begin
      if ruby_command.payload.length < @required_parameters_count
        raise "Get Type parameters mismatch"
      end
      if ruby_command.payload.length > @required_parameters_count
        return Object::const_get(ruby_command.payload[1])
      else
        return Object::const_get(ruby_command.payload[0])
      end
    rescue Exception => e
      return e
    end
  end
end