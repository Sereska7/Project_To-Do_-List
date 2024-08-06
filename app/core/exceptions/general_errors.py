class CustomError(Exception):
    """Базовый класс для общих кастомных ошибок."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DataBaseError(CustomError):
    """Ошибка для случаев, связанных с базой данных."""
    pass


class UnauthorizedError(CustomError):
    """Ошибка для случаев неавторизованного доступа."""
    pass
