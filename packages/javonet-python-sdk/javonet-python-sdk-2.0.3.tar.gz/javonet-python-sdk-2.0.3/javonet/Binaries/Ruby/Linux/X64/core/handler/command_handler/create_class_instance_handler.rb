require_relative 'abstract_command_handler'

class CreateClassInstanceHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 1
  end

  def process(ruby_command)
    return create_class_instance(ruby_command)
  end

  def create_class_instance(ruby_command)
    begin
    if ruby_command.payload.length < @required_parameters_count
      raise "Class instance parameters mismatch"
    end
    if ruby_command.payload.length > 1
      constructor_arguments = ruby_command.payload[1..]
      class_instance = ruby_command.payload[0].send('new', *constructor_arguments)
    else
      class_instance = ruby_command.payload[0].send('new')
    end
    return class_instance
  rescue Exception => e
    return e
  end
  end

end