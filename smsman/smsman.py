import requests
from smsman.errors import ClientError


class Smsman:
    __base_url = "http://api.sms-man.ru/control"
    __method_balance = "/get-balance"
    __method_get_limits = "/limits"
    __method_get_number = "/get-number"
    __method_get_sms = "/get-sms"
    __method_get_all_countries = "/countries"
    __method_get_all_services = "/applications"

    def __init__(self, token, ref="p_moTasn52wq"):
        self.__token = token
        self.__params = {"token": token}
        self.__ref = ref

    def get_balance(self):
        response = requests.get(self.__base_url + self.__method_balance, params=self.__params)
        if "balance" in response.json():
            return float(response.json()['balance'])
        else:
            raise ClientError(response.json()['error_msg'])

    def get_limits(self, country_id=None, application_id=None):
        params = self.__check_params(country_id, application_id)

        response = requests.get(self.__base_url + self.__method_get_limits, params=params)

        return response.json()

    def request_phone_number(self, country_id, application_id):
        params = self.__check_params(country_id, application_id)
        if self.__ref:
            params['ref'] = self.__ref

        response = requests.get(self.__base_url + self.__method_get_number, params=params)
        if "request_id" in response.json() and "number" in response.json():
            return response.json()['request_id'], response.json()["number"]
        else:
            raise ClientError(response.json()['error_msg'])

    def get_sms(self, request_id):
        params = self.__check_params(request_id=request_id)
        response = requests.get(self.__base_url + self.__method_get_sms, params=params)
        if "sms_code" in response.json():
            return response.json()['sms_code']
        else:
            raise ClientError(response.json()['error_msg'])

    def get_all_countries(self):
        response = requests.get(self.__base_url + self.__method_get_all_countries, params=self.__params)
        if "1" in response.json():
            return response.json()
        else:
            raise ClientError(response.json()['error_msg'])

    def get_all_services(self):
        response = requests.get(self.__base_url + self.__method_get_all_services, params=self.__params)
        if "1" in response.json():
            return response.json()
        else:
            raise ClientError(response.json()['error_msg'])

    def __check_params(self, country_id=None, application_id=None, request_id=None):
        params = self.__params
        if country_id:
            params['country_id'] = country_id
        if application_id:
            params['application_id'] = application_id
        if request_id:
            params['request_id'] = request_id

        return params
