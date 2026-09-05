import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.seed_data import seed_database

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    seed_database()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"

def test_dashboard():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue_at_risk" in data
    assert "total_revenue_recovered" in data
    assert "recovery_rate" in data

def test_transactions_list():
    response = client.get("/api/transactions")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) > 0

def test_ai_analyze_and_execution_flow():
    # 1. Fetch demo transaction
    response = client.get("/api/transactions?search=pay_DEMO_UPI_5000")
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) > 0
    tx_id = items[0]["id"]

    # 2. Run AI Analysis
    ai_resp = client.post(f"/api/ai/analyze/{tx_id}")
    assert ai_resp.status_code == 200
    ai_data = ai_resp.json()
    assert ai_data["recommended_action"] == "RETRY"
    assert ai_data["recovery_probability"] >= 0.70

    # 3. Execute Bounded Recovery Action
    exec_resp = client.post(f"/api/recovery/execute/{tx_id}", json={})
    assert exec_resp.status_code == 200
    exec_data = exec_resp.json()
    assert exec_data["success"] == True
    assert exec_data["new_status"] == "RECOVERED"
    assert exec_data["amount_recovered"] == 5000.0

    # 4. Verify Audit Log entry created
    audit_resp = client.get(f"/api/audit-logs?search=pay_DEMO_UPI_5000")
    assert audit_resp.status_code == 200
    audits = audit_resp.json()["items"]
    assert len(audits) > 0
    assert audits[0]["action_taken"] == "RETRY"

def test_safety_rule_max_retries():
    response = client.get("/api/transactions?search=pay_DEMO_RETRY_MAX")
    assert response.status_code == 200
    tx_id = response.json()["items"][0]["id"]

    ai_resp = client.post(f"/api/ai/analyze/{tx_id}")
    assert ai_resp.status_code == 200
    assert ai_resp.json()["recommended_action"] == "HUMAN_ESCALATION"

def test_safety_rule_high_value():
    response = client.get("/api/transactions?search=pay_DEMO_HIGH_VALUE")
    assert response.status_code == 200
    tx_id = response.json()["items"][0]["id"]

    ai_resp = client.post(f"/api/ai/analyze/{tx_id}")
    assert ai_resp.status_code == 200
    assert ai_resp.json()["recommended_action"] == "HUMAN_ESCALATION"

def test_safety_rule_fraud_flag():
    response = client.get("/api/transactions?search=pay_DEMO_FRAUD_FLAG")
    assert response.status_code == 200
    tx_id = response.json()["items"][0]["id"]

    ai_resp = client.post(f"/api/ai/analyze/{tx_id}")
    assert ai_resp.status_code == 200
    assert ai_resp.json()["recommended_action"] == "HUMAN_ESCALATION"
