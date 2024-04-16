from .api import router
from .core.config import settings
from .core.setup import create_application
from .client import router as client_router

app = create_application(router=router, settings=settings)
app.include_router(client_router)
