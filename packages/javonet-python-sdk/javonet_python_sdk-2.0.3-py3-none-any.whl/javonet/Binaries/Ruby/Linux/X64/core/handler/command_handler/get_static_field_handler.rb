require_relative '../../../sdk/core/runtime_lib'
require_relative '../../../sdk/core/ruby_command_type'
require_relative '../../../sdk/core/ruby_command'
require_relative 'abstract_command_handler'

class GetStaticFieldHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 2
  end

  def process(ruby_command)
    return get_static_field(ruby_command)
  end

  def get_static_field(ruby_command)
    begin
    if ruby_command.payload.length != @required_parameters_count
      raise "Static field parameters mismatch"
    end

    merged_value = '@@' + ruby_command.payload[1]
    if ruby_command.payload[0].class_variable_defined?(merged_value)
      response = ruby_command.payload[0].class_variable_get(merged_value)
    else
      response = ruby_command.payload[0].const_get(ruby_command.payload[1])
    end
    return response
    rescue Exception => e
      return e
    end
  end
end
