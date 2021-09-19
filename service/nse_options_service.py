import json
import logging
import requests
import time
from datetime import datetime

# from config.log_config import LogConfig
# from config.msg_config import MessageConfig
from config.app_constants import OPTION_CHAIN_URL_ROOT

log = logging.getLogger(__name__)

# TODO: config classes, exception handling
class NseOptionsService:

    def send_request(self, security_url, headers):
        try:
            with requests.session() as session:
                response = session.get(security_url, headers=headers)
        except requests.exceptions.HTTPError as http_error:
            log.error(http_error)
            raise http_error
        except requests.exceptions.ConnectionError as conn_error:
            log.error(conn_error)
            raise conn_error
        except requests.exceptions.Timeout as timeout_error:
            log.error(timeout_error)
            raise timeout_error
        except requests.exceptions.RequestException as request_exception:
            log.error(request_exception)
            raise request_exception
        except Exception as e:
            log.error(e)
            raise e

        return response

    def get_option_chain(self, security="BANKNIFTY"):
        security_url = OPTION_CHAIN_URL_ROOT + security
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

        response = self.send_request(security_url, headers)
        count = 0
        if not response or response.status_code != 200:
            while response.status_code != 200:
                time.sleep(5)
                response = self.send_request(security_url, headers)
                count += 1
        print(f"Retries: {count}")

        # if response.status_code == 200:
        option_chain = json.loads(response.text)
        current_time = str(datetime.now()).replace('-', '_').replace(':', '_').replace('.', '_')
        # print(f"Option chain: {json.dumps(option_chain)}")

        return option_chain
