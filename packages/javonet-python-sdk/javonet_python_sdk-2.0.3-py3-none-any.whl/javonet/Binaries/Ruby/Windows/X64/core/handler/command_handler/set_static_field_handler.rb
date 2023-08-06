require_relative '../../../sdk/core/runtime_lib'
require_relative '../../../sdk/core/ruby_command_type'
require_relative '../../../sdk/core/ruby_command'
require_relative 'abstract_command_handler'

class  SetStaticFieldHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 3
  end

  def process(ruby_command)
    RubyCommand.new(RuntimeLib::RUBY, RubyCommandType::RESPONSE, [set_static_field(ruby_command)])
  end

  def set_static_field(ruby_command)
    begin
    if ruby_command.payload.length != @required_parameters_count
      raise "Set static field parameters mismatch"
    end

    merged_value = '@@' + ruby_command.payload[1]
    ruby_command.payload[0].class_variable_set(merged_value, ruby_command.payload[2])
    rescue Exception => e
      return e
    end
  end
end