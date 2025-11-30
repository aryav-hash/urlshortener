from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware): # Middleware to log all the HTTP requests and responses
    async def dispatch(self, request: Request, call_next):
        start_time = time.time() # Start timer
        logger.info(f"-> {request.method} {request.url.path}") # Log request
        response = await call_next(request) # Process request
        duration = time.time() - start_time # Calculate duration
        logger.info( # Log response
            f"{request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {duration:.3f}s"
        )

        response.headers["X-Process-Time"] = f"{duration:.3f}" # Add custom header with processing time

        return response
    
def setup_logging(app: FastAPI) -> None:
    app.add_middleware(LoggingMiddleware)
    print("Logging middleware configured")
    
