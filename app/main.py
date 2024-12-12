from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.core.config import settings

def create_app() -> FastAPI:
    """Create a FastAPI app instance."""
    app = FastAPI(
        title=settings.NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )
    
    # Include API routers
    app.include_router(api_router)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
