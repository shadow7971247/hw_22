import pytest
import allure

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.android
@allure.feature("Wikipedia Android")
@allure.story("Search")
@allure.title("Search for film: The Equalizer")
def test_search(driver):

    wait = WebDriverWait(driver, 10)

    with allure.step("Open search"):

        search_icon = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")
            )
        )

        search_icon.click()

        search_input = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.ID,
                    "org.wikipedia.alpha:id/search_src_text"
                )
            )
        )

        search_input.send_keys("The Equalizer")

    with allure.step("Verify search results"):

        results = wait.until(
            EC.presence_of_all_elements_located(
                (
                    AppiumBy.ID,
                    "org.wikipedia.alpha:id/page_list_item_title"
                )
            )
        )

        assert len(results) > 0
        assert "The Equalizer" in results[0].text