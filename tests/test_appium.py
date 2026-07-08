import pytest

from crosslocator import (
    Platform,
    get_current_platform,
    set_current_platform,
    use_appium,
)
from crosslocator.appium import platform_from_capabilities
from crosslocator.platform import set_platform_provider


class FakeDriver:
    def __init__(self, capabilities):
        self.capabilities = capabilities


@pytest.mark.parametrize(
    "caps, expected",
    [
        ({"platformName": "Android"}, Platform.ANDROID),
        ({"platformName": "iOS"}, Platform.IOS),
        ({"platformName": "iOS", "deviceName": "iPad Pro"}, Platform.IPAD),
        ({"appium:platformName": "Windows"}, Platform.WINDOWS),
        ({}, None),
        (None, None),
        ({"platformName": "Symbian"}, None),
    ],
)
def test_platform_from_capabilities(caps, expected):
    assert platform_from_capabilities(caps) is expected


def test_use_appium_drives_resolution(monkeypatch):
    monkeypatch.delenv("CROSSLOCATOR_PLATFORM", raising=False)
    set_current_platform(None)
    use_appium(FakeDriver({"platformName": "Android"}))
    try:
        assert get_current_platform() is Platform.ANDROID
    finally:
        set_platform_provider(None)


def test_use_appium_none_clears_provider(monkeypatch):
    monkeypatch.delenv("CROSSLOCATOR_PLATFORM", raising=False)
    set_current_platform(None)
    use_appium(FakeDriver({"platformName": "iOS"}))
    use_appium(None)
    assert get_current_platform() is None
