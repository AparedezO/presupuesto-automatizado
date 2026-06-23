from fastapi.testclient import TestClient

from app.main import app


def test_materials_search_endpoint_returns_items():
    client = TestClient(app)

    response = client.get("/api/materials", params={"search": "ARAN-P1/2", "limit": 5})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert body["can_create"] is False
    assert any(item["codigo"] == "ARAN-P1/2" for item in body["items"])


def test_materials_search_endpoint_suggests_create_for_missing_term():
    client = TestClient(app)

    response = client.get("/api/materials", params={"search": "Tubo prueba temporal 9/9"})

    assert response.status_code == 200
    body = response.json()
    assert body["can_create"] is True
    assert body["suggested_code"]


def test_apu_draft_endpoint_returns_base_materials():
    client = TestClient(app)

    search_response = client.get("/api/apus", params={"search": "711", "limit": 1})
    assert search_response.status_code == 200
    base = search_response.json()["items"][0]

    response = client.get(f"/api/apus/{base['row_number']}/draft")

    assert response.status_code == 200
    body = response.json()
    assert body["base_codigo_apu"] == base["codigo_apu"]
    assert body["codigo_apu"] == ""
    assert body["detalles"]
    assert all(detail["tipo_item"] == "MATERIAL" for detail in body["detalles"])
    assert not {"E&H", "GLV", "T", "H/C"}.intersection(
        {detail["codigo_item"] for detail in body["detalles"]}
    )


def test_apu_draft_endpoint_returns_formula_quantity_as_text():
    client = TestClient(app)

    response = client.get("/api/apus/941/draft")

    assert response.status_code == 200
    body = response.json()
    formula_detail = next(
        detail for detail in body["detalles"] if detail["codigo_item"] == "BORN-TER 350"
    )
    assert formula_detail["source_row_number"] == 945
    assert formula_detail["cantidad"] == "0"
    assert formula_detail["cantidad_formula"] == "=IFERROR(((F943*2*K945)/J944),0)"
