require 'ffi'
require 'os'
require_relative 'ruby_transmitter_wrapper'

class RubyTransmitter

  def self.send_command(messageArray, messageArrayLen)
    message = FFI::MemoryPointer.new(:uchar, messageArrayLen, true)
    message.put_array_of_uchar(0, messageArray)
    responseArrayLen = RubyTransmitterWrapper.SendCommand(message, messageArrayLen)
    if responseArrayLen >0
      response = FFI::MemoryPointer.new(:uchar, responseArrayLen, true)
      RubyTransmitterWrapper.ReadResponse(response, responseArrayLen)
      responseArray = response.get_array_of_uchar(0, responseArrayLen)
      return responseArray
    else
      raise Exception.new "Javonet native error code: " + responseArrayLen.to_s
    end
  end

  def self.activate_with_licence_file()
    return activate()
  end

  def self.activate_with_credentials(email, licenceKey)
    return activate(email, licenceKey)
  end

  def self.activate_with_credentials_and_proxy(email, licenceKey, proxyHost, proxyUserName, proxyPassword)
    return activate(email, licenceKey, proxyHost, proxyUserName, proxyPassword)
  end

  private_class_method def self.activate(email="", licenceKey="", proxyHost="", proxyUserName="", proxyUserPassword="")
    return RubyTransmitterWrapper.Activate(email, licenceKey, proxyHost, proxyUserName, proxyUserPassword)
  end

end
