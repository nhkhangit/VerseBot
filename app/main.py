# app/main.py
from fastapi import FastAPI
from .core.config import get_settings
from .core.database import get_pool
from .modules import ModuleRegistry
from .modules.projects import ProjectModule
from .modules.tasks import TaskModule

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    version=get_settings().VERSION
)

# Initialize registry with app instance
registry = ModuleRegistry(app)

# Register modules
registry.register_module(ProjectModule)
registry.register_module(TaskModule)

@app.on_event("startup")
async def startup():
    # Initialize database pool
    app.state.pool = await get_pool()
    # Initialize all modules
    await registry.init_all_modules()

@app.on_event("shutdown")
async def shutdown():
    # Cleanup modules
    await registry.cleanup_all_modules()
    # Close database pool
    if hasattr(app.state, 'pool'):
        await app.state.pool.close()

# Register routes for all modules
for module in registry.get_all_modules().values():
    app.include_router(
        module.get_router(),
        prefix=f"{get_settings().API_V1_STR}{module.prefix}",
        tags=module.tags
    )