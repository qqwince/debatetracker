from decimal import Decimal

import pytest

from app.models import User, Game

@pytest.mark.asyncio
async def test_game_create(authorized_client):
    response = await authorized_client.post(
                "api/v1/game",
                json={
                    "entry_creation_date": "2026-09-28T11:13:53.857Z",
                    "tournament_date": "2026-09-28T11:13:53.857Z",
                    "tournament_name": "string",
                    "teammate": "string",
                    "position": "string",
                    "speaker_points": 0,
                    "round_points": 0,
                    "motion_type": "unknown",
                    "motion_theme": "unknown"
                }
            )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_game_create_unauthorized(Client):
    response = Client.post(
                "api/v1/game",
                json={
                    "entry_creation_date": "2026-09-28T11:13:53.857Z",
                    "tournament_date": "2026-09-28T11:13:53.857Z",
                    "tournament_name": "string",
                    "teammate": "string",
                    "position": "string",
                    "speaker_points": 0,
                    "round_points": 0,
                    "motion_type": "unknown",
                    "motion_theme": "unknown"
                }
            )
    assert response.status_code == 401
    

@pytest.mark.asyncio
async def test_game_delete(authorized_client):
    create_game_response = await authorized_client.post(
                    "api/v1/game",
                    json={
                        "entry_creation_date": "2026-09-28T11:13:53.857Z",
                        "tournament_date": "2026-09-28T11:13:53.857Z",
                        "tournament_name": "string",
                        "teammate": "string",
                        "position": "string",
                        "speaker_points": 0,
                        "round_points": 0,
                        "motion_type": "unknown",
                        "motion_theme": "unknown"
                    }
                )
    if not create_game_response.json()['id']:
        assert False
    response = await authorized_client.delete(
                f"api/v1/game?game_id={create_game_response.json()['id']}",
            )
    assert response.status_code == 200
    assert response.json()["_soft_closed"] == True
    assert response.json()["rowcount"] == 1


@pytest.mark.asyncio
async def test_game_change(authorized_client):
    create_game_response = await authorized_client.post(
                    "api/v1/game",
                    json={
                        "entry_creation_date": "2026-09-28T11:13:53.857Z",
                        "tournament_date": "2026-09-28T11:13:53.857Z",
                        "tournament_name": "string",
                        "teammate": "string",
                        "position": "string",
                        "speaker_points": 0,
                        "round_points": 0,
                        "motion_type": "unknown",
                        "motion_theme": "unknown"
                    }
                )
    if not create_game_response.json()['id']:
        assert False
    response = await authorized_client.patch(
                f"api/v1/game?game_id={create_game_response.json()['id']}",
                json={
                    "entry_creation_date": "2027-10-28T11:13:53.857Z",
                    "tournament_date": "2009-01-28T11:13:00.857Z",
                    "tournament_name": "nebo_kochevnika",
                    "teammate": "Matt Caito",
                    "position": "PM",
                    "speaker_points": 84,
                    "round_points": 3,
                    "motion_type": "this_house_opposes",
                    "motion_theme": "kazakhstan"
                }
            )
    assert response.status_code == 200
    assert response.json()["entry_creation_date"] == "2027-10-28T11:13:53.857000Z"
    assert response.json()["tournament_date"] == "2009-01-28T11:13:00.857000Z"
    assert response.json()["tournament_name"] == "nebo_kochevnika"
    assert response.json()["teammate"] == "Matt Caito"
    assert response.json()["position"] == "PM"
    assert response.json()["speaker_points"] == 84
    assert response.json()["round_points"] == 3
    assert response.json()["motion_type"] == "this_house_opposes"
    assert response.json()["motion_theme"] == "kazakhstan"

@pytest.mark.asyncio
async def test_game_get(authorized_client):
    create_game_response = await authorized_client.post(
                    "api/v1/game",
                    json={
                        "entry_creation_date": "2003-10-28T11:13:53.857Z",
                        "tournament_date": "2009-01-28T11:13:00.857Z",
                        "tournament_name": "nebo_kochevnika",
                        "teammate": "Matt Caito",
                        "position": "PM",
                        "speaker_points": 84,
                        "round_points": 3,
                        "motion_type": "this_house_opposes",
                        "motion_theme": "kazakhstan"
                    }
                )
    if not create_game_response.json()['id']:
        assert False
    response = await authorized_client.get(
                f"api/v1/game?game_id={create_game_response.json()['id']}"
            )
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    response = response.json()[0]
    print(f"\n\n\n\n\n\n{response}\n\n\n\n\n\n")
    
    assert response["tournament_name"] == "nebo_kochevnika"
    assert response["teammate"] == "Matt Caito"
    assert response["position"] == "PM"
    assert response["speaker_points"] == 84
    assert response["round_points"] == 3
    assert response["motion_type"] == "this_house_opposes"
    assert response["motion_theme"] == "kazakhstan"
    assert response["tournament_date"] == "2009-01-28T11:13:00.857000"