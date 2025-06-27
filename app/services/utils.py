from app.core.logging import logger
import httpx
from typing import Dict, Any, Optional


async def call_api(endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(endpoint, payload)
            r.raise_for_status()
            return r.json() 
    except httpx.RequestError as e:
        logger.error(f"Lỗi mạng khi gọi API '{endpoint}': {e}", exc_info=True)
        return None
    except httpx.HTTPStatusError as e:
        logger.error(
            f"Lỗi HTTP từ API '{endpoint}': status {e.response.status_code}, response: {e.response.text}", 
            exc_info=True
        )
        return None
    except Exception as e:
        logger.error(f"Lỗi không xác định khi gọi API '{endpoint}': {e}", exc_info=True)
        return None