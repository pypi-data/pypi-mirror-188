require_relative '../interpreter/ruby_interpreter'

class Receiver
  
  def initialize
    @@ruby_interpreter = RubyInterpreter.new
  end

  def send_command(message_array, message_array_len)
    return @@ruby_interpreter.process(message_array, message_array_len)
  end
  
  def heart_beat(message_array, message_array_len)
    response_array = [49,48]
  end
end
