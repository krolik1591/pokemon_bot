from .main_menu import router as main_menu_router
from .battle_handlers import router as battle_router

routers = [
    main_menu_router,
    battle_router
]
