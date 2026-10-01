from decimal import Decimal

import pytest

from app.models import User, Game


def test_user_created_successfully(db_session, Client):
    response = Client.post(
        "api/v1/users/register",
        json={
            "login": "amir",
            "password": "abracadabra"
        } 
    )
    assert response.status_code == 200
    assert response.json()["access_token"] != "abracadabra"
    assert len(response.json()["access_token"]) == 187
    

def test_user_created_wrongly_empty_login(db_session, Client):
    response = Client.post(
        "api/v1/users/register",
        json={
            "login": "    ",
            "password": "abracadabra"
        }
    )
    assert response.status_code == 422
    
    
def test_user_created_wrongly_short_password(db_session, Client):
    response = Client.post(
        "api/v1/users/register",
        json={
            "login": "amir",
            "password": "1"
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_too_short"
    assert response.json()["detail"][0]["msg"] == "String should have at least 6 characters"

@pytest.mark.asyncio
async def test_user_exists(db_session, Client):
    user = User(login="test", password="123456")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    response = Client.post(
            "api/v1/users/register",
            json={
                "login": "test",
                "password": "1223456"
            }
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"