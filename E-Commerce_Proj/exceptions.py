class EngineError(Exception):
    pass

class InvalidInputError(EngineError):
    pass

class OutOfStockError(EngineError):
    pass