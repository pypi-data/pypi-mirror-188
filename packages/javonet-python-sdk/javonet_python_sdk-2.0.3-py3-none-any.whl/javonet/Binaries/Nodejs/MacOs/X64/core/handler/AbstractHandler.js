const Handler = require('./Handler')
const Command = require('../../utils/Command')

class AbstractHandler {
    constructor() {
        if(new.target === AbstractHandler)
            throw new TypeError('You cannot instantiate abstract class')
    }

    process(command) {
        throw new Error('process must be implemented')
    }

    handleCommand(command) {
        this.iterate(command)
        return this.process(command)
    }

    iterate(cmd) {
        for(let i = 0; i < cmd.payload.length; i++) {
            
            if(cmd.payload[i] instanceof Command) {
                let inner = cmd.payload[i]
                cmd.payload[i] = Handler.handlers[inner.commandId].handleCommand(inner)
            }
        }
    }
}

module.exports = AbstractHandler
