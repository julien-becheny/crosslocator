"""Robot Framework integration for crosslocator.

Import in a suite with::

    Library    crosslocator.robot.CrossLocator

Locators are plain Python objects: define them in a Python variable file and
import them, then resolve them with the keywords below.
"""
from __future__ import annotations

from typing import Optional

from .locator import Locator
from .platform import get_current_platform, set_current_platform


class CrossLocator:
    """Robot Framework library exposing crosslocator as keywords."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def set_current_platform(self, platform: str) -> None:
        """Set the platform used to resolve locators.

        Accepts ``android``, ``ios``, ``ipad``, ``windows`` or ``web``.
        """
        set_current_platform(platform)

    def get_current_platform(self) -> str:
        """Return the current platform name, or an empty string if unset."""
        platform = get_current_platform()
        return platform.value if platform is not None else ""

    def resolve_locator(self, locator: Locator, platform: Optional[str] = None) -> str:
        """Resolve a ``Locator`` to a selector string.

        Uses ``platform`` when given, otherwise the current platform.
        """
        if platform:
            return locator.for_platform(platform)
        return locator.resolve()
