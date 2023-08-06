const AbstractHandler = require("./AbstractHandler");

class CreateClassInstanceHandler extends AbstractHandler {
    process(command) {
        let clazz = command.payload[0]
        let methodArguments = command.payload.slice(1)
        return new clazz(...methodArguments)
    }
}

module.exports = new CreateClassInstanceHandler()