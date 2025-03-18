

from app.utils.custom_exceptions import ForbiddenException


def only_owner_action(current_id: int, authorized_id: int, detail="You are not authorized to perform this action"):
    if current_id != authorized_id:
        raise ForbiddenException(detail=detail)