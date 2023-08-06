const AbstractHandler = require("./AbstractHandler");

class GetTypeHandler extends AbstractHandler {
    constructor() {
        super()
    }

    process(command) {
        const { payload } = command
        let typeName = payload[0]
        typeName = typeName.replace(".js", "")
        let type = global[typeName]
        if (type == undefined) {
            throw `Cannot load ${typeName}`
        }
        else { 
            return type
        }

        
    }
}

module.exports = new GetTypeHandler()