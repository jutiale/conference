import datetime
import json

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.config import settings
from app.api.models import Report, Presentation


def test_create_report(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    data = {"name": "Foo", "text": "Bar"}
    response = client.post(
        f"/api/reports/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["text"] == data["text"]
    assert "id" in content


def test_create_presentation(
    client: TestClient, setup_test_data_report: Report, user_token_headers: dict[str, str]
) -> None:
    data = {"room_id": 1, "report_id": 1, 'time_start': "2025-03-20T09:30:00",
            "time_end": "2025-03-20T10:00:00"}
    response = client.post(
        f"/api/presentations/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["room_id"] == data["room_id"]
    assert content["report_id"] == data["report_id"]
    assert content["time_start"] == data["time_start"]
    assert content["time_end"] == data["time_end"]
    assert "id" in content


def test_presentation_time_overlap(
    client: TestClient, setup_test_data_presentation: Presentation, user_token_headers: dict[str, str]
) -> None:
    data = {"room_id": 1, "report_id": 1,
            'time_start': (setup_test_data_presentation.time_start + datetime.timedelta(minutes=10)).isoformat(),
            "time_end": (setup_test_data_presentation.time_end + datetime.timedelta(minutes=10)).isoformat()}
    print(data)
    response = client.post(
        f"/api/presentations/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Time overlap in this room"
