# app/modules/registry.py
from typing import List, Type
from .base.module import BaseModule
from .projects import ProjectModule
from .tasks import TaskModule
from .ui import UIModule  # Thêm UI module

def get_modules() -> List[Type[BaseModule]]:
    """Return list of all available modules"""
    return [
        ProjectModule,
        TaskModule,
        UIModule  # Thêm UI module vào danh sách
    ]