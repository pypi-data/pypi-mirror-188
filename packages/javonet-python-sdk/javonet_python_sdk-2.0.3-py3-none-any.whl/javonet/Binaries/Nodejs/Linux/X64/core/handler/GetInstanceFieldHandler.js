const AbstractHandler = require("./AbstractHandler");

class GetInstanceFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    process(command) {
        const { payload } = command
        let instance = payload[0]
        let field = payload[1]

        return instance[field]
    }
}

module.exports = new GetInstanceFieldHandler()