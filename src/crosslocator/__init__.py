"""crosslocator — define a UI selector once, resolve it on every platform."""
from .locator import (
    CrossLocatorError,
    Locator,
    LocatorNotFound,
    PlatformNotSet,
)
from .platform import (
    Platform,
    get_current_platform,
    set_current_platform,
    set_platform_provider,
)

__version__ = "0.1.0"

__all__ = [
    "Locator",
    "Platform",
    "get_current_platform",
    "set_current_platform",
    "set_platform_provider",
    "CrossLocatorError",
    "LocatorNotFound",
    "PlatformNotSet",
    "__version__",
]
