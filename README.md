# PDF Highlight Extractor

Extract all highlighted text from any PDF — in seconds. Download as plain text, Markdown, or JSON. Built for academics and researchers.

> **Live demo:** https://your-deployment-url.vercel.app
> **Self-host in one command:** `docker compose up`

---

## Features

- Drag-and-drop PDF upload
- Extracts all annotation-based highlights, sorted by page
- Cleans extracted text (fixes ligatures, missing spaces)
- Download results as `.txt`, `.md`, or `.json`
- Search and copy individual highlights in the browser
- PDFs are auto-deleted after 1 hour — no account required
- Self-hostable via Docker for privacy-sensitive institutions

---

## Quick Start

### Use the hosted version

Visit the live URL above — no installation needed.

### Run locally (development)

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload
# API available at http://localhost:8000
# Interactive docs at http://localhost:8000/api/docs
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
# App available at http://localhost:5173
```

### Self-host with Docker

```bash
git clone https://github.com/ddzeeuw1-ai/pdf-highlight-extractor.git
cd pdf-highlight-extractor
docker compose -f docker/docker-compose.yml up
# Open http://localhost:80
```

---

## API

The backend exposes a REST API documented at `/api/docs` (Swagger UI) and `/api/redoc`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload a PDF, returns `upload_id` |
| `POST` | `/api/extract/{upload_id}` | Extract highlights, returns JSON |
| `POST` | `/api/export/{upload_id}?format=txt` | Download formatted highlights |
| `GET`  | `/api/health` | Health check |

**Example**
```bash
# Upload
curl -F "file=@paper.pdf" http://localhost:8000/api/upload

# Extract (use upload_id from above)
curl -X POST http://localhost:8000/api/extract/<upload_id>

# Download as Markdown
curl -X POST "http://localhost:8000/api/export/<upload_id>?format=markdown" -o highlights.md
```

---

## Project Structure

```
pdf-highlight-extractor/
├── backend/          Python FastAPI service
│   ├── app/
│   │   ├── routes/   upload, extract, export endpoints
│   │   ├── services/ pdf_extractor.py + text_cleaner.py
│   │   └── models/   Pydantic schemas
│   ├── tests/
│   └── main.py
├── frontend/         React + TypeScript + Tailwind
│   └── src/
│       ├── components/
│       └── services/
├── docker/           Dockerfile + docker-compose + nginx
└── .github/workflows/ CI tests on every PR
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

---

## Privacy

- Uploaded PDFs are stored only in memory/temp storage and **auto-deleted after 1 hour**
- No file contents are logged
- No account or personal data required
- For complete privacy, self-host using the Docker setup above

---

## License

[MIT](LICENSE)
