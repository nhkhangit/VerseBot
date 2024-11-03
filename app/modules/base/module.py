# app/modules/base/module.py
from fastapi import FastAPI, APIRouter
from typing import Optional, List
from abc import ABC, abstractmethod

class BaseModule(ABC):
    """Base class for all modules"""
    
    def __init__(self, app: Optional[FastAPI] = None):
        self.app = app
        self.router = APIRouter()
        self.prefix: str = ""
        self.tags: List[str] = []
        self.dependencies: List = []

    @abstractmethod
    def register_routes(self) -> None:
        """Register all routes for this module"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the module"""
        pass

    def get_router(self) -> APIRouter:
        """Get configured router for this module"""
        if not self.router.routes:
            self.register_routes()
        return self.router

    async def init_module(self) -> None:
        """Initialize module (e.g., create tables)"""
        pass

    async def cleanup_module(self) -> None:
        """Cleanup module resources"""
        pass