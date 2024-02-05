"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .user_messages import user_messages_router
from .user_callbacks import user_callbacks_router
from .poll_answer import poll_answer_router

routers_list = [
    admin_router,
    user_messages_router,
    poll_answer_router,
    user_callbacks_router,
  
]

__all__ = [
    "routers_list",
]
