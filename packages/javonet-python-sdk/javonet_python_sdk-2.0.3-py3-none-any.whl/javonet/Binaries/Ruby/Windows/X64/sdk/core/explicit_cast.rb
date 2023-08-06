class ExplicitCast
  def cast(value, target_type)
    RubyCommand.new(
      100,
      RubyCommandType::CAST,
      [
        value,
        RubyCommand.new(
          100,
          RubyCommandType::GET_TYPE,
          target_type
        )
      ]
    )
  end
end