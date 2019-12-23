

class DBConnectorError(ConnectionError):
    """DBConnectorException"""
    pass


class DBCreatorError(Exception):
    """DBCreatorException"""
    pass


class DBInserterError(Exception):
    """DBInserterException"""
    pass


class DBIntegrityError(Exception):
    """DBIntegrityError"""
    pass


class ProxyNotSetError(Exception):
    """ProxyNotSetError"""
    pass


class ProxyMaxRequestError(Exception):
    """ProxyMaxRequestError"""
    pass


class ProxyBadConnectionError(Exception):
    """ProxyBadConnectionError"""
    pass
