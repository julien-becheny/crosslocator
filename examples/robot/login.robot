*** Settings ***
Library     crosslocator.robot.CrossLocator
Variables   locators.py

*** Test Cases ***
Resolve Login Selectors On Android
    Set Current Platform    android
    ${username}=    Resolve Locator    ${USERNAME_FIELD}
    ${login}=       Resolve Locator    ${LOGIN_BUTTON}
    Should Be Equal    ${username}    id=com.example:id/username
    Should Be Equal    ${login}       accessibility_id=login

Resolve Login Selectors On iOS
    Set Current Platform    ios
    ${username}=    Resolve Locator    ${USERNAME_FIELD}
    Should Be Equal    ${username}    accessibility_id=username

iPad Falls Back To The iOS Selector
    Set Current Platform    ipad
    ${login}=    Resolve Locator    ${LOGIN_BUTTON}
    Should Be Equal    ${login}    accessibility_id=login
