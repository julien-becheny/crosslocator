"""Example page object: a login screen, defined once for every platform.

Each element is declared a single time, with its selector per platform. There
is no duplication and no `if platform == ...` branching in the test code.
"""
from crosslocator import Locator

USERNAME_FIELD = Locator(
    android="id=com.example:id/username",
    ios="accessibility_id=username",
    windows='//Edit[@AutomationId="username"]',
)

PASSWORD_FIELD = Locator(
    android="id=com.example:id/password",
    ios="accessibility_id=password",
    windows='//Edit[@AutomationId="password"]',
)

LOGIN_BUTTON = Locator(
    android="accessibility_id=login",
    ios="accessibility_id=login",
    windows='//Button[@Name="Log in"]',
    default="id=login",
)
