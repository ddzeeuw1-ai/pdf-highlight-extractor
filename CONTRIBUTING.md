# Contributing to PDF Highlight Extractor

Thank you for your interest in contributing! This project is built by and for researchers, so your domain knowledge is especially valuable.

## How to contribute

**Bug reports and feature requests** — open a GitHub Issue. Use the provided templates. For bugs, include the PDF type (if possible), your OS, and the error message.

**Code contributions** — open an Issue first to discuss the change, then submit a pull request against the `main` branch.

## Development setup

```bash
git clone https://github.com/your-username/pdf-highlight-extractor.git
cd pdf-highlight-extractor

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/         # run tests

# Frontend
cd ../frontend
npm install
npm run dev
```

## Code style

- **Python:** follow PEP 8; run `ruff check backend/` before committing
- **TypeScript:** run `npx tsc --noEmit` before committing
- Write tests for any new backend logic in `backend/tests/`

## Pull request checklist

- [ ] Tests pass (`pytest` and `npm test`)
- [ ] No TypeScript type errors
- [ ] New features documented in README if user-facing
- [ ] One logical change per PR

## Response time

We aim to respond to issues and PRs within 48 hours.
