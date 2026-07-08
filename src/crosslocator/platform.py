"""Platform identification and current-platform state.

crosslocator resolves selectors against a *current platform*. This module owns
the small enum of supported platforms, alias normalization, and the resolution
of the current platform from (in priority order):

1. an explicit value set via :func:`set_current_platform`
2. the ``CROSSLOCATOR_PLATFORM`` environment variable
3. a registered provider (e.g. reading a live Appium session)
"""
from __future__ import annotations

import os
from enum import Enum
from typing import Callable, Optional, Union


class Platform(Enum):
    """A UI platform a selector can target."""

    ANDROID = "android"
    IOS = "ios"
    IPAD = "ipad"
    WINDOWS = "windows"
    WEB = "web"


PlatformLike = Union[Platform, str]

ENV_VAR = "CROSSLOCATOR_PLATFORM"

_ALIASES = {
    "android": Platform.ANDROID,
    "ios": Platform.IOS,
    "iphone": Platform.IOS,
    "ipad": Platform.IPAD,
    "ipados": Platform.IPAD,
    "windows": Platform.WINDOWS,
    "win": Platform.WINDOWS,
    "web": Platform.WEB,
    "browser": Platform.WEB,
}

_current: Optional[Platform] = None
_provider: Optional[Callable[[], Optional[PlatformLike]]] = None


def normalize_platform(value: PlatformLike) -> Platform:
    """Return the :class:`Platform` for ``value``, accepting common aliases.

    Raises :class:`ValueError` for unknown platforms.
    """
    if isinstance(value, Platform):
        return value
    key = str(value).strip().lower()
    try:
        return _ALIASES[key]
    except KeyError:
        raise ValueError(f"Unknown platform: {value!r}") from None


def set_current_platform(value: Optional[PlatformLike]) -> None:
    """Set (or clear, with ``None``) the platform used to resolve selectors."""
    global _current
    _current = None if value is None else normalize_platform(value)


def set_platform_provider(
    provider: Optional[Callable[[], Optional[PlatformLike]]],
) -> None:
    """Register a callable returning the current platform (e.g. from Appium).

    Pass ``None`` to unregister.
    """
    global _provider
    _provider = provider


def get_current_platform() -> Optional[Platform]:
    """Resolve the current platform, or ``None`` if it cannot be determined."""
    if _current is not None:
        return _current
    env = os.environ.get(ENV_VAR)
    if env:
        return normalize_platform(env)
    if _provider is not None:
        result = _provider()
        return None if result is None else normalize_platform(result)
    return None
