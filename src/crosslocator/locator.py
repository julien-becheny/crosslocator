"""The :class:`Locator` type: define a selector once, resolve it per platform."""
from __future__ import annotations

from typing import Dict, Optional

from .platform import (
    Platform,
    PlatformLike,
    get_current_platform,
    normalize_platform,
)


class CrossLocatorError(Exception):
    """Base class for all crosslocator errors."""


class PlatformNotSet(CrossLocatorError):
    """Raised when a resolution needs the current platform but none is set."""


class LocatorNotFound(CrossLocatorError, LookupError):
    """Raised when no selector is available for the requested platform."""


# A platform inherits from the next one in its chain when it has no own selector.
_FALLBACK_CHAINS: Dict[Platform, tuple] = {
    Platform.IPAD: (Platform.IPAD, Platform.IOS),
}


class Locator:
    """A UI selector declared once for several platforms.

    Define a selector per platform plus an optional shared ``default``. At
    runtime, :meth:`resolve` (or :meth:`for_platform`) returns the right
    selector string. crosslocator only *routes* strings — it never parses them
    nor touches your driver.
    """

    __slots__ = ("_selectors", "_default")

    def __init__(
        self,
        *,
        android: Optional[str] = None,
        ios: Optional[str] = None,
        ipad: Optional[str] = None,
        windows: Optional[str] = None,
        web: Optional[str] = None,
        default: Optional[str] = None,
    ) -> None:
        self._selectors: Dict[Platform, Optional[str]] = {
            Platform.ANDROID: android,
            Platform.IOS: ios,
            Platform.IPAD: ipad,
            Platform.WINDOWS: windows,
            Platform.WEB: web,
        }
        self._default = default
        if default is None and not any(self._selectors.values()):
            raise ValueError(
                "A Locator needs at least one platform selector or a default."
            )

    def for_platform(self, platform: PlatformLike) -> str:
        """Return the selector for ``platform``, applying fallbacks.

        Resolution order: the platform's own selector, then its fallback chain
        (e.g. iPad -> iOS), then ``default``. Raises :class:`LocatorNotFound`
        if nothing matches.
        """
        target = normalize_platform(platform)
        for candidate in _FALLBACK_CHAINS.get(target, (target,)):
            value = self._selectors.get(candidate)
            if value is not None:
                return value
        if self._default is not None:
            return self._default
        raise LocatorNotFound(
            f"No selector defined for platform {target.value!r} and no default set."
        )

    def resolve(self) -> str:
        """Return the selector for the current platform.

        Raises :class:`PlatformNotSet` when the current platform is unknown.
        """
        platform = get_current_platform()
        if platform is None:
            raise PlatformNotSet(
                "No current platform set. Use set_current_platform(...) or the "
                "CROSSLOCATOR_PLATFORM environment variable."
            )
        return self.for_platform(platform)

    def __repr__(self) -> str:
        parts = {p.value: v for p, v in self._selectors.items() if v is not None}
        if self._default is not None:
            parts["default"] = self._default
        inner = ", ".join(f"{k}={v!r}" for k, v in parts.items())
        return f"Locator({inner})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Locator):
            return NotImplemented
        return self._selectors == other._selectors and self._default == other._default
