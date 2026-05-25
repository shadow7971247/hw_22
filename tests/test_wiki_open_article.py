import pytest
import allure

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.platform("android")
@allure.feature("Wikipedia Android")
@allure.story("Search")
@allure.title("Search for actor: Denzel Washington")
def test_search_denzel_washington(driver):

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
                    AppiumBy.XPATH,
                    "//*[@resource-id='org.wikipedia.alpha:id/search_src_text']"
                    " | //*[@class='android.widget.EditText']"
                )
            )
        )

        search_input.send_keys("Denzel Washington")

    with allure.step("Verify search results"):

        results = wait.until(
            EC.presence_of_all_elements_located(
                (
                    AppiumBy.XPATH,
                    "//*[@class='android.widget.TextView']"
                )
            )
        )

        assert len(results) > 0