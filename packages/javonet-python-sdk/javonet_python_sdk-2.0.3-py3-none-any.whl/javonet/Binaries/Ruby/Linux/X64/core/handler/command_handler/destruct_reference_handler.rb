require_relative '../../../sdk/core/runtime_lib'
require_relative '../../../sdk/core/ruby_command_type'
require_relative '../../../sdk/core/ruby_command'
require_relative 'abstract_command_handler'
require_relative '../../../core/handler/references_cache'

class DestructReferenceHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 1
  end
  def process(ruby_command)
    begin
      if ruby_command.payload.length == @required_parameters_count
        reference_cache = ReferencesCache.instance
        return reference_cache.delete_reference(ruby_command.payload[0])
      else
        raise "Destruct Reference Handler parameters mismatch"
      end
    rescue Exception => e
      return e
    end
  end
end