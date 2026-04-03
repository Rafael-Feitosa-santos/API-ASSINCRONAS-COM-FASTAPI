from http import HTTPStatus

class NotFoundPostError(Exception):
    def __init__(
        self,
        message: str = "Post não encontrato",
        status_code: int = HTTPStatus.NOT_FOUND
    ) -> None:
        self.message = message
        self.status_code = status_code



class DuplicatePostError(Exception):
    def __init__(self, message: str = "Já existe um post com esse título"):
        self.message = message
        super().__init__(self.message)