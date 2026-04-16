from app.shared.exceptions import NotFoundException


class EndUserNotFoundException(NotFoundException):
    def __init__(self, end_user_id: str) -> None:
        super().__init__(f"End user with id '{end_user_id}' does not exist.")
