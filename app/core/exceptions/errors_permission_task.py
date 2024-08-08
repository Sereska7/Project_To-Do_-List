class PermissionTaskError(Exception):
    """Базовый класс для ошибок, связанных с разрешениями."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PermissionAlreadyExists(PermissionTaskError):
    """Ошибка для случая, когда разрешение для пользователя уже существует."""

    pass


class PermissionNotFound(PermissionTaskError):
    pass
