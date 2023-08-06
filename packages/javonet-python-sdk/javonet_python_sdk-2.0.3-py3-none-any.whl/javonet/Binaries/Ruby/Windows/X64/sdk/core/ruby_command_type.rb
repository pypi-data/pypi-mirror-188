class RubyCommandType
  RESPONSE = 0
  LOAD_LIBRARY = 1
  INVOKE_STATIC_METHOD = 2
  GET_STATIC_FIELD = 3
  SET_STATIC_FIELD = 4
  CREATE_CLASS_INSTANCE = 5
  GET_TYPE = 6
  REFERENCE = 7
  GET_MODULE = 8
  INVOKE_INSTANCE_METHOD = 9
  EXCEPTION = 10
  HEARTBEAT = 11
  CAST = 12
  GET_INSTANCE_FIELD = 13
  OPTIMIZE = 14
  GENERATE_LIB = 15
  INVOKE_GLOBAL_METHOD = 16
  DESTRUCT_REFERENCE = 17


  def self.get_name(command_number)
    if command_number == 0
      return 'RESPONSE'
    end
    if command_number == 1
      return 'LOAD_LIBRARY'
    end
    if command_number == 2
      return 'INVOKE_STATIC_METHOD'
    end
    if command_number == 3
      return 'GET_STATIC_FIELD'
    end
    if command_number == 4
      return 'SET_STATIC_FIELD'
    end
    if command_number == 5
      return 'CREATE_CLASS_INSTANCE'
    end
    if command_number == 6
      return 'GET_TYPE'
    end
    if command_number == 7
      return 'REFERENCE'
    end
    if command_number == 8
      return 'GET_MODULE'
    end
    if command_number == 9
      return 'INVOKE_INSTANCE_METHOD'
    end
    if command_number == 10
      return 'EXCEPTION'
    end
    if command_number == 11
      return 'HEART_BEAT'
    end
    if command_number == 12
      return 'CAST'
    end
    if command_number == 13
      return 'GET_INSTANCE_FIELD'
    end
  end
end