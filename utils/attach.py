import allure
import requests


def add_screenshot(driver):
    png = driver.get_screenshot_as_png()

    allure.attach(
        body=png,
        name='Screenshot',
        attachment_type=allure.attachment_type.PNG
    )


def add_xml(driver):
    xml_dump = driver.page_source

    allure.attach(
        body=xml_dump,
        name='XML screen',
        attachment_type=allure.attachment_type.XML
    )


def add_video(session_id, login, access_key):

    urls = [
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        f'https://api.browserstack.com/automate/sessions/{session_id}.json'
    ]

    video_url = None

    for url in urls:

        try:
            response = requests.get(
                url=url,
                auth=(login, access_key),
                timeout=20
            )

            data = response.json()

            session = (
                data.get('automation_session')
                or data.get('session')
            )

            if session:
                video_url = session.get('video_url')

            if video_url:
                break

        except Exception as e:
            print(f'BrowserStack API error: {e}')

    if not video_url:
        print('BrowserStack video unavailable.')
        return

    allure.attach(
        (
            '<html><body>'
            '<video width="100%" height="100%" controls autoplay>'
            f'<source src="{video_url}" type="video/mp4">'
            '</video>'
            '</body></html>'
        ),
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )