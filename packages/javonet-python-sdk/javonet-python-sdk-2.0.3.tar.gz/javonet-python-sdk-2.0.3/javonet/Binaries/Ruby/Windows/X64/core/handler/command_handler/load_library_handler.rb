require_relative '../../../sdk/core/ruby_command'
require_relative '../../../sdk/core/runtime_lib'
require_relative '../../../sdk/core/ruby_command_type'
require_relative 'abstract_command_handler'

class LoadLibraryHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 1
  end

  def process(ruby_command)
    begin
      if ruby_command.payload.length < @required_parameters_count
        raise Exception.new "Load library method parameters mismatch"
      end
      if ruby_command.payload.length > @required_parameters_count
        assembly_name = ruby_command.payload[1]
      else
        assembly_name = ruby_command.payload[0]
      end
      #noinspection RubyResolve
      require(assembly_name)
      return "Load library success"

    rescue Exception => e
      return "Exception during loading library..." + e.to_s
    end
  end
end