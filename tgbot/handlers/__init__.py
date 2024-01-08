"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .simple_menu import menu_router
from .user_messages import user_messages_router
from .user_callbacks import user_callbacks_router

routers_list = [
    admin_router,
    menu_router,
    user_messages_router,
    user_callbacks_router,
]

__all__ = [
    "routers_list",
]
