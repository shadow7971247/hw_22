import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Config(BaseModel):
    browserstack_username: str = os.getenv("BROWSERSTACK_USERNAME", "")
    browserstack_access_key: str = os.getenv("BROWSERSTACK_ACCESS_KEY", "")

    browserstack_url: str = os.getenv(
        "BROWSERSTACK_URL",
        "https://hub-cloud.browserstack.com/wd/hub"
    )

    timeout: int = int(os.getenv("TIMEOUT", "10"))

    android_device: str = os.getenv("ANDROID_DEVICE", "Google Pixel 7")
    android_version: str = os.getenv("ANDROID_VERSION", "13.0")
    android_app: str = os.getenv("ANDROID_APP", "bs://sample.app")

    ios_device: str = os.getenv("IOS_DEVICE", "iPhone 14 Pro Max")
    ios_version: str = os.getenv("IOS_VERSION", "16")
    ios_app: str = os.getenv(
        "IOS_APP",
        "bs://7aaf6afaa432c2931e2381680c1d0c7f6a0ee2d5"
    )


config = Config()