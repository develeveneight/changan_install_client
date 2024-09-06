import os

import requests
from dotenv import load_dotenv

from helpers.logger import Cl
from helpers import helper

load_dotenv()


class baseModelApi:
    """
    Base class for all api endpoints.
    """

    def __init__(self):
        self.lang = helper.set_language()
        self.url = os.getenv('SERVER_API_URL')
        if os.name == "nt":
            self.settings_path = os.path.join(os.getenv('LOCALAPPDATA'), 'changan_install')
            self.token_path = os.path.join(self.settings_path, 'token')
        self.token = None
        self.headers = {}

    def set_token(self, token):
        self.token = token

    def api_request(self, api_url, method, data=None, files=None, json_response=True):
        self.headers = {'Authorization': f'Bearer {self.token}'}
        if json_response:
            self.headers['Accept'] = 'application/json'
        if files and data:
            response = requests.request(method, api_url, data=data, files=files, headers=self.headers)
        elif data:
            response = requests.request(method, api_url, data=data, headers=self.headers)
        elif files:
            response = requests.request(method, api_url, files=files, headers=self.headers)
        else:
            response = requests.request(method, api_url, headers=self.headers)
        if response.status_code == 200:
            # print(response.text)
            return response.json()
        else:
            # print(response.text)
            print(
                f"{Cl.red}API request cannot be processed. Status code: {response.status_code}\n{response.json()['message']}")
            # exit()


class User(baseModelApi):
    def __init__(self):
        super().__init__()

    def registration(self, email: str, password: str) -> dict:
        """
        Registration
        :param email:
        :param password:
        :return: User data
        """
        api_url = self.url + '/signup'
        payload = {
            'email': email,
            'password': password,
        }
        response = requests.post(api_url, data=payload)
        if response.status_code == 200:
            print(self.lang.REG_SUCCESS)
            return self.authenticate(email, password)
        else:
            # print(response.text)
            print(self.lang.REG_FAILED.format(Cl.red, Cl.reset))
            return {}

    def authenticate(self, email, password) -> dict:
        """
        Authenticate
        :param email:
        :param password:
        :return: User data
        """
        api_url = self.url + '/signin'
        payload = {
            'email': email,
            'password': password,
        }

        response = requests.post(api_url, data=payload)
        # print(response.text)

        if response.status_code == 200:
            # self.token = response.json().get('token')
            print(self.lang.AUTH_SUCCESS)
            # return response.json().get('user')
            return response.json()
        else:
            print(self.lang.AUTH_FAILED.format(Cl.red, Cl.reset))
            return {'error': "1", 'message': 'Authentication failed'}


class Job(baseModelApi):
    def __init__(self):
        super().__init__()
        self.url += '/job'

    def get(self, job_id: int):
        """
        Get job status
        :return:
        """
        payload = {
            'job_id': job_id,
        }
        api_url = f'{self.url}/get/{job_id}'
        return self.api_request(api_url, method='post', data=payload)

    def get_all(self):
        """
        Get all jobs
        TODO: unnecessary for client, move to watcher JobExtended
        :return:
        """
        api_url = self.url + '/get_all'
        return self.api_request(api_url, 'post')


class Certificate(baseModelApi):
    def __init__(self):
        super().__init__()
        self.url += '/certificate'

    def upload_system_app(self, headunit_uid: str, system_app: str) -> dict:
        """
        Upload system app
        :param headunit_uid:
        :param system_app:
        :return:
        """
        payload = {
            'headunit_uid': headunit_uid,
        }
        system_app_dict = {
            'system_app': system_app,
        }
        api_url = self.url + '/upload_system_app'
        return self.api_request(api_url, method='POST', data=payload, files=system_app_dict)

    def get_parameters(self, headunit_uid: str) -> dict:
        """
        Get certificate parameters
        :param headunit_uid:
        :return:
        """
        payload = {
            'headunit_uid': headunit_uid
        }
        api_url = self.url + '/get_parameters'
        return self.api_request(api_url, method='POST', data=payload)

    def download(self, headunit_uid: str, os_prop: str, version_date: str) -> str | dict:
        """
        Download certificate files in zip
        :param headunit_uid:
        :param os_prop:
        :param version_date:
        :return: url if all ok, dict with error message if error
        """
        payload = {
            'headunit_uid': headunit_uid,
            'os_prop': os_prop.strip().replace(" ", "_"),
            'version_date': version_date.strip().replace(" ", "_"),
        }
        api_url = self.url + '/download'
        return self.api_request(api_url, method='POST', data=payload)


class Car(baseModelApi):
    def __init__(self):
        super().__init__()
        self.url += '/car'

    def save_car_data(self, data: dict) -> dict:
        """
        Save car data
        :param data:
        :return:
        """
        api_url = self.url + '/save_car_data'
        return self.api_request(api_url, method='POST', data=data)

    def get_cars(self, user_id: int) -> dict:
        """
        archived
        TODO: remove from client
        :param user_id:
        :return:
        """
        payload = {
            'user_id': user_id
        }
        api_url = self.url + '/get_cars'
        return self.api_request(api_url, method='post', data=payload)

    def get_car_by_headunit_uid(self, headunit_uid: str) -> dict:
        """
        Get car by headunit uid
        :param value:
        :return: car data
        """
        payload = {
            'headunit_uid': headunit_uid
        }
        api_url = self.url + '/get_car_by_headunit_uid'
        return self.api_request(api_url, method='post', data=payload)

    def rename(self, headunit_uid: str, name: str) -> dict:
        """
        Rename car
        :param headunit_uid:
        :param name:
        :return:
        """
        payload = {
            'headunit_uid': headunit_uid,
            'name': name
        }
        api_url = self.url + '/rename_car'
        return self.api_request(api_url, method='post', data=payload)


class Apk(baseModelApi):
    def __init__(self):
        super().__init__()
        self.url += '/apk'

    def upload(self, file_paths: list, headunit_uid: str) -> dict:
        """
        Upload apk
        :param file_paths:
        :param headunit_uid:
        :return:
        """
        payload = {
            "headunit_uid": headunit_uid
        }
        api_url = self.url + '/upload_apks'
        # load files
        files = [('files[]', (open(file, 'rb'))) for file in file_paths]
        return self.api_request(api_url, method='post', files=files, data=payload)

    def install(self, headunit_uid: str, apk_name: str) -> dict:
        """
        Request for concrete apks from server
        :param headunit_uid:
        :param apk_name:
        :return: job data
        """
        payload = {
            'headunit_uid': headunit_uid,
            'apk_name': apk_name
        }
        api_url = self.url + '/custom_install'
        return self.api_request(api_url, method='post', data=payload)

    def save_data(self, package_name: str, apk_path: str, headunit_uid: str) -> dict:
        """
        Save info about installation
        :param package_name:
        :param apk_path:
        :param headunit_uid:
        :return:
        """
        payload = {
            'headunit_uid': headunit_uid,
            'package_name': package_name,
            'apk_path': apk_path
        }
        api_url = self.url + '/save_data'
        return self.api_request(api_url, method='post', data=payload)

    def get_installed_apk(self, headunit_uid: str):
        """
        Get list of installed apks on car with headunit_uid
        :param headunit_uid:
        :return:
        """
        payload = {
            'headunit_uid': headunit_uid,
        }
        api_url = self.url + '/get_installed_apks'
        return self.api_request(api_url, method='post', data=payload)


class Payment(baseModelApi):
    def __init__(self):
        super().__init__()

    def create_payment(self, headunit_uid: str) -> dict:
        """
        Payment create request
        :param headunit_uid:
        :return: Payment data
        """
        payload = {
            "headunit_uid": headunit_uid
        }
        api_url = self.url + '/create_payment'
        return self.api_request(api_url, method='post', data=payload)

    def get_payment_status(self, user_id: str, payment_id: str) -> dict:
        """
        Get payments status from payment service
        :param user_id: user id from payment data
        :param payment_id: if from payment data
        :return:
        """
        payload = {
            'user_id': user_id,
            'payment_id': payment_id
        }
        api_url = self.url + '/get_payment_status'
        return self.api_request(api_url, method='post', data=payload)


class ServerInfo(baseModelApi):
    def __init__(self):
        super().__init__()
        self.url += '/'

    def check_url(self):
        url = os.getenv('SERVER_API_URL')
        return requests.get(url).status_code


if __name__ == '__main__':
    pass
