from fastapi import APIRouter
from server_src.get_models_tests_route import router as get_models_and_tests_router
from server_src.run_tests_route import router as run_tests_router

router = APIRouter()
router.include_router(get_models_and_tests_router)
router.include_router(run_tests_router)


@router.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}
