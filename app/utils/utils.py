
from fastapi import HTTPException, status


def only_owner_action(current_id: int, authorized_id: int):
    if current_id != authorized_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")