const { Handler } = require('../handler/Handler')
const CommandEncoder = require('../protocol/CommandEncoder')
const CommandDecoder = require('../protocol/CommandDecoder')


let Transmitter

class Interpreter {
    handler = new Handler()

    execute(command, connectionType, tcpAddress) {
        // lazy transmitter loading
        if(!Transmitter) {
            Transmitter = require('../transmitter/NodejsTransmitter')
        }

        let encoder = new CommandEncoder()
        let byteMessage = encoder.encode(command,connectionType, tcpAddress)

        let bytes = Transmitter.sendCommand(byteMessage)
        return new CommandDecoder(bytes).decode()
    }

    process(byteArray) {
        let decoder = new CommandDecoder(byteArray)
        let command = decoder.decode()

        return this.handler.handleCommand(command)
    }
}

module.exports = Interpreter
