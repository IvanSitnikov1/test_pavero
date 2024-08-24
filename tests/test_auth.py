import pytest
from sqlalchemy import insert, select

from conftest import client, async_session_maker


def test_register():
    response = client.post("/auth/register", json={
        "email": "string1",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "date_of_birth": "2024-08-24",
        "phone_number": "string"
    })

    assert response.status_code == 201
