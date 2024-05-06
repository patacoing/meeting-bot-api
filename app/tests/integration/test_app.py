from uuid import UUID

from fastapi import status


def test_read_root_should_return_200_when_ping(client):
    response = client.post(
        "/",
        json={
            "type": 1,
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"type": 1}


def test_read_root_should_return_200_when_plan(client):
    response = client.post(
        "/",
        json={
            "type": 3,
            "data": {
                "name": "plan",
                "options": [
                    {
                        "type": 3,
                        "name": "date",
                        "value": "28/02"
                    },
                    {
                        "type": 3,
                        "name": "time",
                        "value": "00:50"
                    },
                    {
                        "type": 3,
                        "name": "description",
                        "value": "Sprint backlog"
                    }
                ]
            }
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "type": 4,
        "data": {
            "content": f"Meeting meeting-{UUID('00000000-0000-0000-0000-000000000000')} planned for 28/02 at 00:50 - "
                       f"Sprint backlog"
        }
    }


def test_read_root_should_return_200_when_cancel(client):
    response = client.post(
        "/",
        json={
            "type": 3,
            "data": {
                "name": "cancel",
                "options": [
                    {
                        "type": 3,
                        "name": "name",
                        "value": "meeting-b989e429-4ffc-492f-b245-7fb12412c2fc"
                    }
                ]
            }
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "type": 4,
        "data": {
            "content": f"Meeting meeting-b989e429-4ffc-492f-b245-7fb12412c2fc cancelled"
        }
    }


def test_read_root_should_return_422_when_unknown_command(client):
    response = client.post(
        "/",
        json={
            "type": 3,
            "data": {
                "name": "unknown",
                "options": []
            }
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
