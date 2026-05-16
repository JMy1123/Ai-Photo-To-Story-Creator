# AI Photo To Story Creator

A functional AI-powered image-to-prompt generator.

## Features

- Upload any image
- Generate prompts in multiple formats
- Descriptive mode
- Casual descriptive mode
- Straightforward mode
- Stable Diffusion prompt mode
- MidJourney prompt mode
- e621 tag generation
- Adjustable response lengths
- Optional max word count

## Tech Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- FastAPI
- OpenAI Vision API

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Run backend:

```bash
uvicorn main:app --reload
```

Backend runs at:

```txt
http://127.0.0.1:8000
```

### Frontend

Open:

```txt
frontend/index.html
```

## Prompt Modes

- Descriptive
- Descriptive Casual
- Straightforward
- Stable Diffusion
- MidJourney
- e621 Tags

## Planned Features

- Negative prompt generation
- SDXL optimization
- Multi-prompt generation
- Prompt history
- Prompt export system
- React frontend upgrade
- User accounts
- Cloud deployment
