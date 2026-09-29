from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.exporters import save_pdf

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "ComicCraft" in response.text

def test_pdf_export_handles_panel_text_after_wide_image(tmp_path, monkeypatch):
    monkeypatch.setattr("app.exporters.EXPORTS_DIR", tmp_path)
    image_path = tmp_path / "wide-panel.png"
    Image.new("RGB", (1000, 100), "white").save(image_path)
    layout = [{
        "panel_number": 1,
        "title": "A Test Panel",
        "image_path": str(image_path),
        "scene_description": "A detailed scene description " * 40,
        "caption": "A short caption.",
        "narration": "A short narration.",
        "dialogue": "A short line of dialogue.",
    }]

    pdf_path = save_pdf(layout)

    assert (tmp_path / pdf_path.rsplit("/", 1)[-1]).is_file()
