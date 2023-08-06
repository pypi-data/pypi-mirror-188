import requests
from multiprocessing.synchronize import Lock
import multiprocessing as mp
from dataclasses import dataclass
from time import sleep
import logging as log
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .errors import AdsError
from .configs import UserProxyConfig, FingepringConfig


@dataclass
class AdsApi:
    base_url_ads: str
    lock: Lock = mp.Lock()

    def request(self, endpoint: str, params: dict | None = None, data: dict | None = None, attempts: int = 5):
        req_info = f'request {self.base_url_ads+endpoint}\n data = {data}\n params = {params}\n'
        for attempt in range(attempts):
            try:
                self.lock.acquire()
                sleep(1)  # because limite 1 request per second
                response = requests.get(
                    self.base_url_ads + endpoint, params=params, data=data).json()
                self.lock.release()
            except:
                log.error(f'Error with {req_info}-- {traceback.format_exc()}')
            if response["code"] != 0:
                raise AdsError(response["msg"])
            log.info(f'Success request to ads {req_info}response = {response}')
            return response['data']

    def query_group(self, page_size: int = 100, group_name: str | None = None, page: int = 1) -> list[dict]:
        resp = self.request(
            '/api/v1/group/list', params={'page_size': page_size, 'page': page, 'group_name': group_name})
        resp = resp['list']
        return resp

    def update_group(self, group_id: int, group_name: str) -> None:
        resp = self.request(
            '/api/v1/group/update', data={'group_id': group_id, 'group_name': group_name})

    def create_group(self, group_name: str) -> dict:
        resp = self.request('/api/v1/group/create',
                            data={'group_name': group_name})
        return resp

    def open_browser(self, user_id: str, serial_number: str | None = None,
                     open_tabs: int = 0, ip_tab: int = 1, launch_args: str | None = None, headless: int = 0,
                     disable_password_filling: int = 0, clear_cache_after_closing: int = 0, enable_password_saving: str = 0) -> dict:
        resp = self.request('/api/v1/browser/start', params={'user_id': user_id, 'serial_number': serial_number, 'open_tabs': open_tabs,
                                                             'ip_tab': ip_tab, 'launch_args': launch_args, 'headless': headless,
                                                             'disable_password_filling': disable_password_filling, 'clear_cache_after_closing': clear_cache_after_closing,
                                                             'enable_password_saving': enable_password_saving})
        return resp

    def close_browser(self, user_id: str, serial_number: int | None = None) -> None:
        resp = self.request(
            '/api/v1/browser/stop', params={'user_id': user_id, 'serial_number': serial_number})

    def check_open_status(self, user_id: str, serial_number: int | None = None) -> dict:
        resp = self.request('/api/v1/browser/active',
                            params={'user_id': user_id, 'serial_number': serial_number})
        return resp

    def create_account(self, name: str | None = None, domain_name: int | None = None, open_urls: list[str] | None = None,
                       repeat_config: list[int] | None = None, username: str | None = None, password: str | None = None,
                       cookie: str | None = None, ignore_cookie_error: int = 0, group_id: int | None = None, ip: str | None = None,
                       country: str | None = None, city: str | None = None, remark: str | None = None,
                       user_proxy_config: dict = UserProxyConfig().dict(), fingerprint_config: dict =FingepringConfig().dict()) -> dict:
        resp = self.request('/api/v1/user/create',
                            data={'name': name, 'domain_name': domain_name, 'open_urls':open_urls, 'repeat_config':repeat_config, 'username':username,
                                    'password':password, 'cookie':cookie, 'ignore_cookie_error':ignore_cookie_error, 'group_id':group_id,
                                    'ip':ip, 'country':country, 'city':city, 'remark':remark, 'user_proxy_config':user_proxy_config,
                                    'fingerprint_config':fingerprint_config})
        return resp

    def update_account(self, name: str, domain_name: int | None = None, open_urls: list[str] | None = None,
                       repeat_config: list[int] | None = None, username: str | None = None, password: str | None = None,
                       cookie: str | None = None, ignore_cookie_error: int = 0, group_id: int | None = None, ip: str | None = None,
                       country: str | None = None, city: str | None = None, remark: str | None = None,
                       user_proxy_config: dict = UserProxyConfig().dict(), fingerprint_config: dict =FingepringConfig().dict()) -> dict:
        resp = self.request('/api/v1/user/update',
                            data={'name': name, 'domain_name': domain_name, 'open_urls':open_urls, 'repeat_config':repeat_config, 'username':username,
                                    'password':password, 'cookie':cookie, 'ignore_cookie_error':ignore_cookie_error, 'group_id':group_id,
                                    'ip':ip, 'country':country, 'city':city, 'remark':remark, 'user_proxy_config':user_proxy_config,
                                    'fingerprint_config':fingerprint_config})
        return resp

    def query_account(self, group_id:int|None = None, user_id:str|None = None, serial_number:int|None = None, page:int=1, page_size:int = 1) -> list[dict]:
        resp = self.request('/api/v1/user/list',
                            params={'group_id': group_id, 'user_id': user_id, 'serial_number':serial_number, 'page':page, 'page_size':page_size})
        return resp['list']

    def delete_account(self, user_ids:list[int]) -> dict:
        resp = self.request('/api/v1/user/delete',
                            data={'user_ids': user_ids})
        return resp


    def update_account_group(self, user_ids:list[int], group_id:int) -> dict:
        resp = self.request('/api/v1/user/regroup',
                            data={'user_ids': user_ids, 'group_id':group_id})
        return resp


    def connect_ads_to_selenium(self, user_id:int) -> webdriver.Chrome:
        data = self.open_browser(user_id=user_id)
        chrome_driver = data["webdriver"]
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", data["ws"]["selenium"])
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        driver.get("https://www.baidu.com")
        return driver