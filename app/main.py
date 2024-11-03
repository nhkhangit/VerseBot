# app/main.py
from fastapi import FastAPI
from .core.config import get_settings
from .core.database import get_pool
from .modules import ModuleRegistry
from .modules.registry import get_modules
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title=get_settings().PROJECT_NAME,
        version=get_settings().VERSION
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize registry
    registry = ModuleRegistry(app)
    
    # Register all modules
    modules = get_modules()
    for module_class in modules:
        registry.register_module(module_class)

    @app.on_event("startup")
    async def startup():
        app.state.pool = await get_pool()
        await registry.init_all_modules()

    @app.on_event("shutdown")
    async def shutdown():
        await registry.cleanup_all_modules()
        if hasattr(app.state, 'pool'):
            await app.state.pool.close()

    # Register routes for all modules
    for module in registry.get_all_modules().values():
        if module.name != "ui":  # API modules get prefix
            app.include_router(
                module.get_router(),
                prefix=f"{get_settings().API_V1_STR}{module.prefix}",
                tags=module.tags
            )
        else:  # UI module without prefix
            app.include_router(
                module.get_router(),
                tags=module.tags
            )

    return app

app = create_app()