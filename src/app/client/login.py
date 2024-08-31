from fastapi import Request, APIRouter, Depends, Response

from .config import templates

router = APIRouter(tags=["client_login"])


@router.get("/login")
async def admin_login_page(request: Request):
    return templates.TemplateResponse("auth/login_page.html", {"request": request})
