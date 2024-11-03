# app/modules/__init__.py
from typing import Dict, Type
from fastapi import FastAPI
from .base.module import BaseModule

class ModuleRegistry:
    def __init__(self, app: FastAPI):
        self.app = app
        self._modules: Dict[str, BaseModule] = {}

    def register_module(self, module_class: Type[BaseModule]) -> None:
        """Register a module class and initialize it with the app instance"""
        module = module_class(self.app)
        self._modules[module.name] = module

    def get_module(self, name: str) -> BaseModule:
        return self._modules.get(name)

    def get_all_modules(self) -> Dict[str, BaseModule]:
        return self._modules

    async def init_all_modules(self) -> None:
        for module in self._modules.values():
            await module.init_module()

    async def cleanup_all_modules(self) -> None:
        for module in self._modules.values():
            await module.cleanup_module()