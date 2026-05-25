import os
import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from config import config
from utils import attach


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "platform(name): mobile platform (android / ios)"
    )


def build_options(platform):

    common_bstack = {
        "userName": config.browserstack_username,
        "accessKey": config.browserstack_access_key,
        "appiumVersion": "2.0.0",
    }

    if platform == "android":

        options = UiAutomator2Options()

        options.set_capability("platformName", "Android")
        options.set_capability("automationName", "UiAutomator2")
        options.set_capability("deviceName", config.android_device)
        options.set_capability("platformVersion", config.android_version)
        options.set_capability("app", config.android_app)

        options.set_capability(
            "bstack:options",
            common_bstack
        )

    elif platform == "ios":

        options = XCUITestOptions()

        options.set_capability("platformName", "iOS")
        options.set_capability("automationName", "XCUITest")

        options.set_capability("browserName", "Safari")

        options.set_capability(
            "bstack:options",
            {
                **common_bstack,
                "deviceName": config.ios_device,
                "osVersion": config.ios_version,
            }
        )

    else:
        raise ValueError(f"Unknown platform: {platform}")

    return options


@pytest.fixture(scope="function")
def driver(request):

    marker = request.node.get_closest_marker("platform")

    if marker is None:
        raise RuntimeError(
            "Use @pytest.mark.platform('android'|'ios')"
        )

    marker_platform = marker.args[0].lower()
    env_platform = os.getenv("PLATFORM")

    if env_platform:
        env_platform = env_platform.lower()

        if env_platform != marker_platform:
            raise RuntimeError(
                f"Platform mismatch: "
                f"marker={marker_platform}, env={env_platform}"
            )

    platform = env_platform or marker_platform

    options = build_options(platform)

    driver = webdriver.Remote(
        command_executor=config.browserstack_url,
        options=options
    )

    driver.implicitly_wait(config.timeout)

    yield driver

    try:
        attach.add_screenshot(driver)
        attach.add_xml(driver)

        attach.add_video(
            driver.session_id,
            config.browserstack_username,
            config.browserstack_access_key
        )

    finally:
        driver.quit()