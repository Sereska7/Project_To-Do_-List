import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(ac: AsyncClient):
    response = await ac.post("/register",
                             json={
                                 "email": "test1@example.com",
                                 "hash_password": "string"
                             })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_user(ac: AsyncClient):
    response = await ac.post("/login",
                             json={
                                 "email": "test1@example.com",
                                 "hash_password": "string"
                             })
    assert response.status_code == 404
