# Examples

These examples use a generic **login screen** and need no real device. They
resolve the same locators on several platforms to show what crosslocator does.

## Python

```bash
cd examples/python
python demo.py
```

Prints the same page object resolved for Android, iOS, iPadOS and Windows —
notice iPad falls back to the iOS selector, and Windows uses the shared default.

## Robot Framework

Requires Robot Framework:

```bash
pip install robotframework
robot examples/robot/login.robot
```

The suite resolves locators for Android, iOS and iPadOS and asserts the expected
selector strings — a self-contained check that the Robot Framework integration
works end to end.
