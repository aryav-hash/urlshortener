from fastapi import FastAPI
from app.config import settings
from app.api import routes
from app.middleware import (
    setup_cors,
    setup_logging,
    setup_error_handlers
)

app = FastAPI(
    debug=settings.debug
)

setup_error_handlers(app)
setup_cors(app)
setup_logging(app)

app.include_router(routes.router)

@app.get("/")
async def root():
    """ Root endpoint for API Information """
    return {
        "message": "URL Shortener API",
        "version": "1.0.0",
        "base_url": settings.base_url,
        "endpoints": {
            "shorten": "/api/shorten",
            "redirect": "/{short_code}",
        }
    }
