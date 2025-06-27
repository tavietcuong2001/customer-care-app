from fastapi import APIRouter
from app.schemas.chat import Query, Response
from app.services.chat import get_response

router = APIRouter()

@router.post("/response", response_model=Response)
async def get_response_function(query: Query):
    response = await get_response(
        query.query,
        query.chat_history,
        query.service,
        query.chat_id
    )
    
    return response