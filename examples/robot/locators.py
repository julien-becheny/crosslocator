"""Robot Framework variable file: exposes Locator objects as suite variables.

Imported from login.robot via `Variables   locators.py`. Each name becomes a
Robot scalar variable, e.g. ${USERNAME_FIELD}.
"""
from crosslocator import Locator

USERNAME_FIELD = Locator(
    android="id=com.example:id/username",
    ios="accessibility_id=username",
)

PASSWORD_FIELD = Locator(
    android="id=com.example:id/password",
    ios="accessibility_id=password",
)

LOGIN_BUTTON = Locator(
    android="accessibility_id=login",
    ios="accessibility_id=login",
    default="id=login",
)
