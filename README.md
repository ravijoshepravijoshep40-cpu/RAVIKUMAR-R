# ComicCraft — AI Comic Story Creator

A complete FastAPI + Jinja2 application based on the supplied 23-page ComicCraft specification.

## Workflow

1. User enters story prompt, character name, setting, tone and art style.
2. Gemini Flash generates a structured 5-panel outline.
3. Gemini Pro expands the outline into narration and dialogue.
4. Stable Diffusion generates an illustration for each panel.
5. `layout_builder.py` combines images and story data.
6. `exporters.py` creates a multi-page PDF.
7. The preview page displays the comic and provides a PDF download.
8. The export-success page confirms the workflow.

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── css/style.css
│   ├── panels/
│   └── exports/
├── assets/fonts/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows setup

```powershell
cd ComicCraft
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your Gemini API key.

Then run:

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## macOS/Linux

```bash
cd ComicCraft
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## API example

POST `/generate-comic/json`

```json
{
  "story_prompt": "A brave fox exploring an enchanted forest",
  "character_name": "Lumi",
  "setting": "Forest",
  "tone": "Dramatic",
  "art_style": "Anime"
}
```

POST `/test-image`

```json
{
  "prompt": "anime comic illustration of a brave fox in an enchanted forest"
}
```

## AI image options

### Option A — Hugging Face API
Set:

```env
HF_API_KEY=...
USE_LOCAL_DIFFUSERS=false
```

### Option B — Local Stable Diffusion
Set:

```env
USE_LOCAL_DIFFUSERS=true
```

A suitable GPU is strongly recommended. The first run downloads the model and can require substantial disk space and VRAM.

### Demo mode

The default `.env.example` enables:

```env
ALLOW_DEMO_FALLBACK=true
```

This means the website can be tested without AI keys. It uses deterministic demo story data and placeholder images. Set it to `false` when you want configuration failures to be reported instead of falling back.

## Important note about model names

The supplied project document specifies `gemini-1.5-flash`, `gemini-1.5-pro`, and `runwayml/stable-diffusion-v1-5`. This implementation keeps those names in `.env` so they can be changed without modifying source code if your provider/account no longer exposes a specified model.

## Security

- Never commit `.env`.
- Do not put API keys into HTML/JavaScript.
- API keys are read server-side only.
