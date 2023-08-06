let CommandType = require('./CommandType')

class Command {
    constructor(runtime, commandType, payload = []) {
        this.runtime = runtime
        this.commandId = commandType
        this.payload = payload
    }

    createResponse(...args) {
        return new Command(
            this.runtime,
            CommandType.Response,
            [...args]
        )
    }

    createReference(...args) {
        return new Command(
            this.runtime,
            CommandType.Reference,
            [...args]
        )
    }

    dropFirstPayloadArg() {
        return new Command(
            this.runtime,
            this.commandId,
            this.payload.slice(1)
        )
    }

    addArgToPayload(arg) {
        return new Command(
            this.runtime,
            this.commandId,
            this.payload.concat(arg)
        )
    }
    
    appendArgument(arg) {
        return new Command(
            this.runtime,
            this.commandId,
            [arg].concat(this.payload)
        )
    }
}

module.exports = Command