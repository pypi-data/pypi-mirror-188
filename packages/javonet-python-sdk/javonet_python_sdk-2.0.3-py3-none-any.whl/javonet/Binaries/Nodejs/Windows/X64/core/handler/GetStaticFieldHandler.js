const AbstractHandler = require("./AbstractHandler");

class GetStaticFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    process(command) {
        const { payload } = command
        let type = payload[0]
        let field = payload[1]

        return type[field]
    }
}


module.exports = new GetStaticFieldHandler()