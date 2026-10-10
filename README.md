# AI Appointment Booking Agent

A full-stack AI-powered appointment booking app built with FastAPI for the backend and React + Vite for the frontend. The assistant can help users find available therapy appointment slots and retrieve therapist information using OpenAI function calling.

## Tech Stack

- Backend: Python, FastAPI
- Frontend: React, Vite
- AI: OpenAI Responses API
- Tools: Custom slot lookup and therapist details functions

## Project Structure

```text
AI Appointment Booking Agent -FastAPI/
├── backend/
│   ├── .env
│   ├── .gitignore
│   ├── agent.py
│   ├── main.py
│   ├── requirements.txt
│   ├── schemas.py
│   ├── tools.py
│   └── venv/
├── frontend/
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── vite.config.js
├── README.md
└── .gitignore
```

## Features

- AI chat interface for appointment booking questions
- FastAPI backend with CORS enabled for local frontend development
- OpenAI-powered agent using tool calling
- Therapist detail lookup
- Appointment slot retrieval for a given date

## Prerequisites

- Python 3.13+
- Node.js 18+
- npm
- An OpenAI API key

## Backend Setup

From the project root:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder if it does not already exist:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Run the backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- http://localhost:8000/
- http://localhost:8000/chat

## Frontend Setup

From the project root:

```bash
cd frontend
npm install
npm run dev
```

The frontend will run at:

- http://localhost:5173

## API Example

Example chat request body:

```json
{
  "message": "I want to book a therapy appointment for tomorrow.",
  "history": []
}
```

Example response:

```json
{
  "response": "Here are the available slots..."
}
```

## Notes

- The backend currently allows requests from `http://localhost:5173`.
- The AI tool layer is intentionally simple and can be extended with real scheduling, database, or CRM integrations.
- Keep your `OPENAI_API_KEY` in the backend `.env` file and avoid committing secrets to source control.

## License

This project is for educational/demo purposes unless otherwise specified by the repository owner.
