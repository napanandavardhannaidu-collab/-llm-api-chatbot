import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google.genai import errors

from app.memory import ConversationMemory
from app.llm_client import generate_response


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FastAPI application
app = FastAPI(
    title="DevBot API",
    description="AI DevOps Assistant powered by Google Gemini",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://172.18.246.151:5500"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Conversation memory
memory = ConversationMemory(max_messages=10)


class ChatRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=10000)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to DevBot API",
        "status": "running",
        "provider": "Google Gemini"
    }


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    conversation_id = request.conversation_id
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    history = memory.get_history(conversation_id)

    try:
        response = generate_response(history, user_message)

        if not response or not response.strip():
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response"
            )

        # Save messages only after successful generation
        memory.add_message(conversation_id, "user", user_message)
        memory.add_message(conversation_id, "assistant", response)

        return {
            "conversation_id": conversation_id,
            "response": response
        }

    except HTTPException:
        raise

    except errors.APIError as exc:

        logger.exception("Gemini API error")

        # Gemini service temporarily unavailable
        if exc.code == 503:
            raise HTTPException(
                status_code=503,
                detail="Gemini is currently experiencing high demand. Please try again later."
            )

        # API quota exceeded
        if exc.code == 429:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again after the quota resets."
            )

        # Authentication errors
        if exc.code in (401, 403):
            raise HTTPException(
                status_code=502,
                detail="Gemini API authentication failed. Check your API key."
            )

        # Timeout errors
        if exc.code in (408, 504):
            raise HTTPException(
                status_code=504,
                detail="Gemini API request timed out. Please try again."
            )

        # Other Gemini API errors
        raise HTTPException(
            status_code=502,
            detail="Gemini API could not process your request."
        )

    except TimeoutError:
        logger.exception("Gemini request timed out")

        raise HTTPException(
            status_code=504,
            detail="Request timed out. Please try again."
        )

    except Exception:
        logger.exception("Unexpected AI service error")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again."
        )


# Get conversation history
@app.get("/history/{conversation_id}")
def get_history(conversation_id: str):
    return {
        "conversation_id": conversation_id,
        "history": memory.get_history(conversation_id)
    }


# Delete conversation history
@app.delete("/history/{conversation_id}")
def delete_history(conversation_id: str):
    memory.clear_history(conversation_id)

    return {
        "message": "Conversation history cleared",
        "conversation_id": conversation_id
    }
