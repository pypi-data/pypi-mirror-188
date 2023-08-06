require_relative '../protocol/command_serializer'
require_relative '../protocol/command_deserializer'
require_relative '../handler/ruby_handler'

class RubyInterpreter
  def execute(ruby_command, connection_type, tcp_address)
    require_relative '../transmitter/ruby_transmitter'
    command_serializer = CommandSerializer.new
    message = command_serializer.encode(ruby_command, connection_type, tcp_address)
    response_byte = RubyTransmitter.send_command(message,message.length)
    command_deserializer = CommandDeserializer.new(response_byte,response_byte.length)
    received_command = command_deserializer.decode
    return received_command
  end

  def process(byte_array, byte_array_len)
    command_deserializer = CommandDeserializer.new(byte_array,byte_array_len)
    received_command = command_deserializer.decode
    ruby_handler = RubyHandler.new
    command_serializer = CommandSerializer.new
    return command_serializer.encode(ruby_handler.handle_command(received_command), 0, "0.0.0.0:0")
  end
end
