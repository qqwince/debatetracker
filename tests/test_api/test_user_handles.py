
import pytest

from app.models import User


@pytest.mark.asyncio
async def test_user_created_successfully(db_session, client):
    response = await client.post(
        "api/v1/users/register", json={"login": "amir", "password": "abracadabra"}
    )
    assert response.status_code == 200
    assert response.json()["access_token"] != "abracadabra"


@pytest.mark.asyncio
async def test_user_created_wrongly_empty_login(db_session, client):
    response = await client.post(
        "api/v1/users/register", json={"login": "    ", "password": "abracadabra"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_user_created_wrongly_short_password(db_session, client):
    response = await client.post(
        "api/v1/users/register", json={"login": "amir", "password": "1"}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_too_short"
    assert (
        response.json()["detail"][0]["msg"]
        == "String should have at least 6 characters"
    )


@pytest.mark.asyncio
async def test_user_already_exists(db_session, client):
    user = User(login="test", password="123456")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    response = await client.post(
        "api/v1/users/register", json={"login": "test", "password": "1223456"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


@pytest.mark.asyncio
async def test_user_logined_wrong_password(db_session, client):
    await client.post(
        "api/v1/users/register", json={"login": "amir", "password": "abracadabra"}
    )

    response = await client.post(
        "api/v1/users/login", json={"login": "amir", "password": "wrong_password"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_logined_wrong_login(db_session, client):
    await client.post(
        "api/v1/users/register", json={"login": "amir", "password": "abracadabra"}
    )

    response = await client.post(
        "api/v1/users/login",
        json={"login": "amirijfjiajijfiojioafsjiofj-0214ub", "password": "abracadabra"},
    )
    assert response.status_code == 401
    