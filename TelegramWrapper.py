import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class TelegramWrapper:

    def __init__(self, telegram_chat_id, telegram_token):
        self.telegram_chat_id = telegram_chat_id
        self.telegram_token = telegram_token

        self.retry_strategy = Retry(
            total=4,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["POST", "GET", "HEAD"],
            backoff_factor=10
        )
        self.adapter = HTTPAdapter(max_retries=self.retry_strategy)

    def send_message(self, text):
        url="https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}".format(self.telegram_token, text, self.telegram_chat_id)
        http = requests.Session()
        http.mount("https://", self.adapter)
        http.mount("http://", self.adapter)
        response = http.post(url)
        content = response.content.decode("utf8")
        return content

    def send_photo(self, imgPath):
        files = {
            'photo': open(imgPath, 'rb')
        }
        http = requests.Session()
        http.mount("https://", self.adapter)
        http.mount("http://", self.adapter)
        url="https://api.telegram.org/bot{}/sendPhoto?chat_id={}".format(self.telegram_token, self.telegram_chat_id)
        response = http.post(url, files=files)
        print(response)
        content = response.content.decode("utf8")
        time.sleep(0.5)
        return content
