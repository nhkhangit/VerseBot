# app/modules/ui/__init__.py
from fastapi import FastAPI, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ..base.module import BaseModule

class UIModule(BaseModule):
    def __init__(self, app: FastAPI = None):
        super().__init__(app)
        self.prefix = ""  # Empty prefix for root URL
        self.tags = ["ui"]

    @property
    def name(self) -> str:
        return "ui"

    def register_routes(self) -> None:
        # Mount static files
        static_path = Path(__file__).parent / "static"
        self.app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
        
        # Setup templates
        templates_path = Path(__file__).parent / "templates"
        self.templates = Jinja2Templates(directory=str(templates_path))

        @self.router.get("/", tags=["ui"])
        async def index(request: Request):
            """Serve the main UI page"""
            return self.templates.TemplateResponse(
                "index.html",
                {"request": request}
            )

    async def init_module(self) -> None:
        pass