# crosslocator

**Define a UI selector once. Resolve it on every platform.**

Cross-platform test automation means maintaining the same element for Android,
iOS, iPadOS, Windows and the web. Most teams end up either duplicating selectors
or scattering `if platform == ...` branches through their page objects.

`crosslocator` lets you declare a selector **once**, per platform, and resolves
the right one at runtime — from **pure Python (Appium), Robot Framework, or any
other framework**. It only routes selector *strings*; it never wraps your driver.

```python
from crosslocator import Locator

ADD_PATIENT = Locator(
    android="accessibility_id=add_patient",
    ios="add_patient",
    windows='//Button[@Name="Add"]',
    default="id=add",
)

ADD_PATIENT.for_platform("ios")   # -> "add_patient"
```

## Installation

```bash
pip install crosslocator
```

Zero runtime dependencies.

## Why

- **One source of truth** per element — no duplicated selectors, no platform `if/else`.
- **Framework-agnostic** — Appium in plain Python, Robot Framework, or anything else.
- **Sensible fallbacks** — iPad inherits from iOS, and a shared `default` covers the rest.
- **Typed** and dependency-free.

## Quick start (Python)

```python
from crosslocator import Locator, set_current_platform

ADD_PATIENT = Locator(
    android="accessibility_id=add_patient",
    ios="add_patient",
    windows='//Button[@Name="Add"]',
)

set_current_platform("android")   # usually done once, at session start
ADD_PATIENT.resolve()             # -> "accessibility_id=add_patient"
```

## Robot Framework

```robotframework
*** Settings ***
Library     crosslocator.robot.CrossLocator
Variables   locators.py        # ADD_PATIENT defined as a Locator here

*** Test Cases ***
Open Add Patient
    Set Current Platform    android
    ${selector}=    Resolve Locator    ${ADD_PATIENT}
    # -> pass ${selector} to AppiumLibrary / Browser as usual
```

## How the platform is resolved

`resolve()` determines the current platform in this order:

1. an explicit `set_current_platform(...)`
2. the `CROSSLOCATOR_PLATFORM` environment variable
3. a registered provider — typically an Appium session (see below)

## Automatic platform detection (Appium)

Let crosslocator read the platform straight from a live Appium session, so you
never call `set_current_platform` by hand.

**Python (Appium-Python-Client):**

```python
from crosslocator import use_appium

use_appium(driver)      # your Appium webdriver
LOGIN_BUTTON.resolve()  # platform detected from the session capabilities
```

**Robot Framework (AppiumLibrary):**

```robotframework
Open Application    ${REMOTE_URL}    platformName=Android    ...
Use Appium Session
${selector}=    Resolve Locator    ${LOGIN_BUTTON}
```

iPad is detected from the session device name and resolves to iPad selectors
(falling back to iOS when none are defined).

## Fallback rules

- `ipad` → falls back to `ios` when no iPad-specific selector is set
- any platform → falls back to `default`
- nothing found → `LocatorNotFound`

## Examples

Runnable examples (no device needed) live in the [`examples/`](examples/) folder —
a login screen resolved across Android, iOS, iPadOS and Windows, plus a Robot
Framework suite.

## Roadmap

- **v0.1:** the core `Locator` type, platform resolution, Robot Framework keywords.
- **v0.2 (current):** automatic platform detection from a live Appium session.
- **Next:** Playwright/Browser helpers, and declarative loading of whole screens from YAML/dict.

Issues and contributions are welcome.

## License

MIT © 2026 Julien Becheny
