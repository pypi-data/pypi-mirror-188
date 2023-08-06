require_relative '../../../sdk/core/runtime_lib'
require_relative '../../../sdk/core/ruby_command_type'
require_relative '../../../sdk/core/ruby_command'
require_relative '../references_cache'
require_relative 'abstract_command_handler'

class ResolveInstanceHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 1
  end
  def process(ruby_command)
    return resolve_reference(ruby_command)
  end

  def resolve_reference(ruby_command)
    if ruby_command.payload.length != @required_parameters_count
      raise "Resolve Instance parameters mismatch"
    end
    begin
      references_cache = ReferencesCache.instance
      return references_cache.resolve_reference(ruby_command.payload[0])
    rescue Exception => ex
      return ex
    end
  end
end