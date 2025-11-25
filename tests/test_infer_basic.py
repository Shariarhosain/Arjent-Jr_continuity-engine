from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_infer_sequence_increments():
    payload = {
        "tenant_id": "t1",
        "user_id": "u1",
        "session_id": "s1",
        "sequence_id": 1,
        "message": "Hello",
    }
    r1 = client.post("/infer", json=payload)
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["sequence_id"] == 1
    assert "continuity_signature" in d1

    payload["sequence_id"] = 1
    payload["message"] = "Second"
    r2 = client.post("/infer", json=payload)
    d2 = r2.json()
    assert d2["sequence_id"] == 2
