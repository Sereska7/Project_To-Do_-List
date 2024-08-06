class TaskError(Exception):
    """Базовый класс для ошибок, связанных с задачами."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class TaskNotFound(TaskError):
    """Ошибка для случая, когда задача не найдена."""
    pass


class NotOwnerError(TaskError):
    """Ошибка для случая, когда пользователь не является владельцем задачи."""
    pass
