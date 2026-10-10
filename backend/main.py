from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import ChatRequest, ChatResponse
from agent import run_agent


# --------------------------------
# Create FastAPI application
# --------------------------------

app = FastAPI(
    title="AI Appointment Booking Agent API",
    description="Backend API for an AI-powered therapy appointment booking agent",
    version="1.0.0"
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# Home endpoint
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Appointment Booking Agent API is running"
    }


# --------------------------------
# Chat endpoint
# --------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    history = [
        item.model_dump()
        for item in request.history
    ]

    answer = run_agent(
        user_message=request.message,
        history=history
    )

    return {
        "response": answer
    }
