from .battle_handlers import router as battle_router
from .other_handlers import router as other_router
from .pre_battle_handlers import router as pre_battle_router

routers = [
    battle_router,
    other_router,
    pre_battle_router
]
