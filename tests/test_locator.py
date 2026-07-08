import pytest

from crosslocator import Locator, LocatorNotFound, PlatformNotSet, set_current_platform


def test_for_platform_returns_specific_selector():
    loc = Locator(android="id=add", ios="add_btn")
    assert loc.for_platform("android") == "id=add"
    assert loc.for_platform("ios") == "add_btn"


def test_ipad_falls_back_to_ios():
    loc = Locator(ios="add_btn")
    assert loc.for_platform("ipad") == "add_btn"


def test_ipad_prefers_its_own_selector():
    loc = Locator(ios="add_btn", ipad="ipad_add")
    assert loc.for_platform("ipad") == "ipad_add"


def test_default_used_when_platform_missing():
    loc = Locator(android="id=add", default="id=fallback")
    assert loc.for_platform("windows") == "id=fallback"


def test_missing_selector_raises():
    loc = Locator(android="id=add")
    with pytest.raises(LocatorNotFound):
        loc.for_platform("windows")


def test_resolve_uses_current_platform():
    loc = Locator(android="id=add", ios="add_btn")
    set_current_platform("ios")
    try:
        assert loc.resolve() == "add_btn"
    finally:
        set_current_platform(None)


def test_resolve_without_platform_raises():
    loc = Locator(android="id=add")
    set_current_platform(None)
    with pytest.raises(PlatformNotSet):
        loc.resolve()


def test_empty_locator_is_rejected():
    with pytest.raises(ValueError):
        Locator()


def test_repr_is_readable():
    loc = Locator(android="id=add", default="id=x")
    assert repr(loc) == "Locator(android='id=add', default='id=x')"
