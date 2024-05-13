from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from .config import templates

router = APIRouter(tags=["client_landing"])

@router.get("/", response_class=HTMLResponse)
async def get_landing(request: Request):
    return templates.TemplateResponse(
            "landing/landing.html",
            {
                "request": request,
            },
        )
