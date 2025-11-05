from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server_src.router import router

app = FastAPI(
    title="SEMOSS Playground Testing API",
    description="API for testing SEMOSS functionality",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint providing basic API information"""
    return {
        "message": "SEMOSS Playground Testing API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8888, reload=True)
