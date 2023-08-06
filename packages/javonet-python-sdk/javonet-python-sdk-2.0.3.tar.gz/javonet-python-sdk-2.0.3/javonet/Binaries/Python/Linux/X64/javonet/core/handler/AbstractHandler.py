class AbstractHandler:
    def HandleCommand(self, python_command):
        raise NotImplementedError('subclasses must override HandleCommand()!')
