from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.user import User
from app.schemas.ai import AIQuestion, AIAnswer
from app.services.ai import ai_service

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


@router.post("/ask", response_model=AIAnswer)
async def ask_ai(
    data: AIQuestion,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    Ask AI assistant a question about the dataset.

    The AI will use the database content to answer your questions about:
    - Cars (plate numbers, models, years, colors)
    - Drivers (names, license numbers, phone numbers)
    - Provinces, Cities, Villages
    - Relationships between these entities

    Query parameters:
    - format: Response format - 'plain' (default), 'markdown', or 'html'

    Requires authentication.
    """
    try:
        # Get raw answer from AI
        raw_answer, context = await ai_service.answer_question(data.question, session)

        # Format the response based on user request
        formatted_answer = ai_service.format_response(raw_answer, data.format)

        return AIAnswer(answer=formatted_answer, context=context, format=data.format)
    except ValueError:
        print("There is an error with AI model")
