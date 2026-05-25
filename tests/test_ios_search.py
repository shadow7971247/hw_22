import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ios
@pytest.mark.platform("ios")
@allure.feature("Wikipedia iOS Web")
@allure.story("Search")
def test_ios_search_equalizer(driver):

    wait = WebDriverWait(driver, 20)

    driver.get("https://www.wikipedia.org")

    search_input = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.NAME, "search")
        )
    )

    search_input.send_keys("The Equalizer")

    driver.find_element(
        AppiumBy.XPATH,
        "//button[@type='submit']"
    ).click()

    wait.until(
        EC.presence_of_element_located(
            (
                AppiumBy.XPATH,
                "//*[contains(text(),'Equalizer')]"
            )
        )
    )

    assert "Equalizer" in driver.page_source