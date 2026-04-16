from app.shared.exceptions import ConflictException, NotFoundException


class OrderNotFoundException(NotFoundException):
    def __init__(self, order_id: str) -> None:
        super().__init__(f"Order with id '{order_id}' does not exist.")


class OrderAlreadyCancelledException(ConflictException):
    def __init__(self, order_id: str) -> None:
        super().__init__(f"Order '{order_id}' has already been cancelled.")


class OrderAlreadyDeliveredException(ConflictException):
    def __init__(self, order_id: str) -> None:
        super().__init__(f"Order '{order_id}' has already been delivered.")


class OutsideDeliveryRangeException(ConflictException):
    def __init__(self, distance_km: float) -> None:
        super().__init__(
            f"The delivery address is {distance_km:.1f}km away and is outside the delivery range."
        )
