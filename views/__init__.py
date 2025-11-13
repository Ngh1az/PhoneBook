"""
Views package for PhoneBook Application
"""

from .login_view import LoginView
from .register_view import RegisterView
from .dashboard_view import DashboardView
from .contact_view import ContactView
from .group_view import GroupView
from .tag_view import TagView
from .trash_view import TrashView
from .profile_view import ProfileView

__all__ = [
    "LoginView",
    "RegisterView",
    "DashboardView",
    "ContactView",
    "GroupView",
    "TagView",
    "TrashView",
    "ProfileView",
]
