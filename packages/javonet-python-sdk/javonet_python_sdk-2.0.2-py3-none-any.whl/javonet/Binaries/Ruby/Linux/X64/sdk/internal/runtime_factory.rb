require_relative 'abstract/abstract_runtime_factory'
require_relative 'connection_type'
require_relative 'runtime_context'

class RuntimeFactory < AbstractRuntimeFactory

  def initialize(connection_type, tcp_address = nil)
    @connection_type = connection_type
    if @connection_type == ConnectionType::TCP
      if tcp_address.nil?
        raise("Error tcp ip adress is not given!")
      end
    end
    @tcp_address = tcp_address
  end

  def clr
    RuntimeContext.get_instance(RuntimeLib::CLR, @connection_type, @tcp_address )
  end

  def go
    RuntimeContext.get_instance(RuntimeLib::GO, @connection_type, @tcp_address )
  end

  def jvm
    RuntimeContext.get_instance(RuntimeLib::JVM, @connection_type, @tcp_address )
  end

  def netcore
    RuntimeContext.get_instance(RuntimeLib::NETCORE, @connection_type, @tcp_address )
  end

  def perl
    RuntimeContext.get_instance(RuntimeLib::PERL, @connection_type, @tcp_address )
  end

  def ruby
    RuntimeContext.get_instance(RuntimeLib::RUBY, @connection_type, @tcp_address )
  end

  def nodejs
    RuntimeContext.get_instance(RuntimeLib::NODEJS, @connection_type, @tcp_address )
  end

  def python
    RuntimeContext.get_instance(RuntimeLib::PYTHON, @connection_type, @tcp_address )
  end

end