const AbstractHandler = require("./AbstractHandler");
const ReferencesCache = require("./ReferencesCache")

class DestructReferenceHandler extends AbstractHandler {

    constructor() {
        super()
    }

    process(command) {
        let cache = ReferencesCache.getInstance()
        return cache.deleteReference(command.payload[0])
    }
}

module.exports = new DestructReferenceHandler()