require_relative 'runtime_lib'
require_relative 'ruby_command_type'

class RubyCommand
  def initialize(runtime_lib, command_type, payload)
    @runtime_lib = runtime_lib
    @command_type = command_type
    @payload = payload
  end

  def runtime_lib
    @runtime_lib
  end

  def command_type
    @command_type
  end

  def payload
    @payload
  end

  def to_string
    'Runtime Library: ' + RuntimeLib.get_name(@runtime_lib).to_s + ' ' + 'Ruby command type: ' +  RubyCommandType.get_name(@command_type).to_s + ' ' + 'with parameters: '+ @payload.to_s
  end

  def drop_first_payload_argument
    payload_args = []
    payload_args = payload_args + @payload
    if payload_args.length != 0
      payload_args.delete_at(0)
    end
    return RubyCommand.new(@runtime_lib, @command_type, payload_args)

  end

  def add_arg_to_payload(argument)
    merged_payload = payload + [argument]
    return RubyCommand.new(@runtime_lib, @command_type, merged_payload)
  end

  def add_arg_to_payload_on_beginning(argument)
    merged_payload = [argument] + payload
    return RubyCommand.new(@runtime_lib, @command_type, merged_payload)
  end


  def eql?(other)
    @is_equal = false
    if self == other
      @is_equal = true
    end
    if other == nil or self.class != other.class
      @is_equal = false
    end
    if self.command_type == other.command_type and self.runtime_lib == other.runtime_lib
      @is_equal = true
    end
    if payload.length == other.payload.length
      i = 0
    array_item_equal = false
    for payload_item in payload
      if payload_item.eql? other.payload[i]
        array_item_equal = true
      else
        array_item_equal = false
      end
      i += 1
    end
      @is_equal = array_item_equal
    else
      @is_equal = false
    end
      return @is_equal
  end
end