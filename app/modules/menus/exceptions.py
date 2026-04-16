from app.shared.exceptions import NotFoundException


class MenuNotFoundException(NotFoundException):
    def __init__(self, tenant_id: str) -> None:
        super().__init__(f"Menu for tenant '{tenant_id}' does not exist.")


class MenuSectionNotFoundException(NotFoundException):
    def __init__(self, section_id: str) -> None:
        super().__init__(f"Menu section with id '{section_id}' does not exist.")


class MenuItemNotFoundException(NotFoundException):
    def __init__(self, item_id: str) -> None:
        super().__init__(f"Menu item with id '{item_id}' does not exist.")


class MenuItemUnavailableException(NotFoundException):
    def __init__(self, item_id: str) -> None:
        super().__init__(f"Menu item '{item_id}' is not currently available.")
