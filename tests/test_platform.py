import pytest

from crosslocator import Platform, get_current_platform, set_current_platform
from crosslocator.platform import ENV_VAR, normalize_platform, set_platform_provider


def test_normalize_aliases():
    assert normalize_platform("Android") is Platform.ANDROID
    assert normalize_platform("iPadOS") is Platform.IPAD
    assert normalize_platform("win") is Platform.WINDOWS


def test_unknown_platform_raises():
    with pytest.raises(ValueError):
        normalize_platform("symbian")


def test_explicit_platform_takes_priority(monkeypatch):
    monkeypatch.setenv(ENV_VAR, "android")
    set_current_platform("ios")
    try:
        assert get_current_platform() is Platform.IOS
    finally:
        set_current_platform(None)


def test_env_var_used_when_no_explicit(monkeypatch):
    set_current_platform(None)
    monkeypatch.setenv(ENV_VAR, "windows")
    assert get_current_platform() is Platform.WINDOWS


def test_provider_used_as_last_resort(monkeypatch):
    set_current_platform(None)
    monkeypatch.delenv(ENV_VAR, raising=False)
    set_platform_provider(lambda: "android")
    try:
        assert get_current_platform() is Platform.ANDROID
    finally:
        set_platform_provider(None)
