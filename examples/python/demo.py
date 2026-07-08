"""Resolve the same page object on several platforms.

Run from this folder::

    python demo.py

Notice that iPad falls back to the iOS selector, and Windows uses the shared
default when no Windows-specific selector applies.
"""
from crosslocator import set_current_platform

from locators import LOGIN_BUTTON, PASSWORD_FIELD, USERNAME_FIELD

ELEMENTS = {
    "Username field": USERNAME_FIELD,
    "Password field": PASSWORD_FIELD,
    "Login button": LOGIN_BUTTON,
}


def show_for(platform: str) -> None:
    set_current_platform(platform)
    print(f"\n== {platform} ==")
    for name, locator in ELEMENTS.items():
        print(f"  {name:16} -> {locator.resolve()}")


if __name__ == "__main__":
    for current in ("android", "ios", "ipad", "windows"):
        show_for(current)
