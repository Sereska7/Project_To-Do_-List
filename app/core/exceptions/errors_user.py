class UserError(Exception):
    """Базовый класс для ошибок, связанных с пользователями."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFound(UserError):
    """Ошибка для случая, когда пользователь не найден."""

    pass


class UserAlreadyExists(UserError):
    """Ошибка для случая, когда пользователь уже существует."""

    pass


class InvalidPasswordError(UserError):
    """Ошибка для случая, когда пароль не верный."""

    pass


class TokenNotFound(UserError):
    """Ошибка для случая, когда токен не найден."""

    pass


class UserHasNoPermission(UserError):
    """У пользователя нет прав доступа к задаче"""

    pass
