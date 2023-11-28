from .battle_handlers import router as battle_router
from .other_handlers import router as other_router

routers = [
    battle_router,
    other_router
]
