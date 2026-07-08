"""Automatic platform detection from a live Appium session.

crosslocator stays framework-agnostic: this module only reads the session
capabilities and translates them into a :class:`~crosslocator.platform.Platform`.
"""
from __future__ import annotations

from typing import Any, Mapping, Optional

from .platform import Platform, set_platform_provider


def platform_from_capabilities(
    capabilities: Optional[Mapping[str, Any]],
) -> Optional[Platform]:
    """Translate Appium capabilities into a :class:`Platform`.

    Returns ``None`` when the platform cannot be determined.
    """
    if not capabilities:
        return None
    name = str(
        capabilities.get("platformName")
        or capabilities.get("appium:platformName")
        or ""
    ).strip().lower()
    device = str(
        capabilities.get("deviceName")
        or capabilities.get("appium:deviceName")
        or ""
    ).lower()
    if name == "android":
        return Platform.ANDROID
    if name in ("ios", "iphoneos", "iphone os"):
        return Platform.IPAD if "ipad" in device else Platform.IOS
    if name in ("windows", "win"):
        return Platform.WINDOWS
    return None


def use_appium(driver: Optional[Any]) -> None:
    """Detect the current platform automatically from an Appium ``driver``.

    Registers a provider that reads ``driver.capabilities`` on each resolution,
    so you no longer need to call :func:`set_current_platform` by hand. Pass
    ``None`` to stop using the driver.
    """
    if driver is None:
        set_platform_provider(None)
        return

    def provider() -> Optional[Platform]:
        return platform_from_capabilities(getattr(driver, "capabilities", None))

    set_platform_provider(provider)
