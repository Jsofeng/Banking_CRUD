import pytest
from models import User
from fastapi import HTTPException
from main import require_admin

@pytest.mark.asyncio
async def test_require_admin_non_admin():
    user = User(
        username="Jonathan",
        email="jonathan.j@gmail.com",
        role="user"
    )

    with pytest.raises(HTTPException) as exc: #expect an HTTPException since role != admin
        require_admin(user)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Not authorized"

