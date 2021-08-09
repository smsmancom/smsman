import requests
from smsman.errors import WrongTokenError, SMSnotReceivedError


class Smsman:
    __base_url = "http://api.sms-man.ru/control"
    __method_balance = "/get-balance"
    __method_get_limits = "/limits"
    __method_get_number = "/get-number"
    __method_get_sms = "/get-sms"
    __method_get_all_countries = "/countries"
    __method_get_all_services = "/applications"

    def __init__(self, token: str, ref="p_moTasn52wq"):
        """
        :param token: Your Token from sms-man.com
        :param ref: Your referal code
        """

        self.__token = token
        self.__params = {"token": token}
        self.__ref = ref

    def get_balance(self):
        """
        Information about your balance in RUB

        GET /get-balance

        :return: The amount of your balance, RUB
        :rtype: float
        """

        response = requests.get(self.__base_url + self.__method_balance, params=self.__params)

        if "balance" in response.json():
            return float(response.json()['balance'])
        else:
            raise WrongTokenError(response.json()['error_msg'])

    def get_limits(self, country_id=None, application_id=None):
        """
        Information about amount of available numbers in counry for service
        If country_id is None or application_id is None send information about
        all countries and applications

        :param country_id: id of country, str
        :param application_id: if of application, str
        :return: The amount of available numbers
        :rtype: json
        """

        params = self.__check_params(country_id, application_id)

        response = requests.get(self.__base_url + self.__method_get_limits, params=params)

        return response.json()

    def request_phone_number(self, country_id: str, application_id: str):
        """
        Queries the phone number by country id and service id.
        Returns request number (needed to receive sms) and phone number.

        :param country_id: id of country. Can check list on web-site or with method get_all_countries
        :param application_id: id of application. Can check list on web-site or with method get_all_services
        :return: request_id, number
        :rtype: str, str
        """

        params = self.__check_params(country_id, application_id)

        if self.__ref:
            params['ref'] = self.__ref

        response = requests.get(self.__base_url + self.__method_get_number, params=params)

        if "request_id" in response.json() and "number" in response.json():
            return response.json()['request_id'], response.json()["number"]
        else:
            raise WrongTokenError(response.json()['error_msg'])

    def get_sms(self, request_id: str):
        """
        Texts out the request number.
        If the SMS has not yet arrived, an error will be returned.

        :param request_id: Number of ID (get with phone number)
        :return: sms_code
        :rtype: str
        """

        params = self.__check_params(request_id=request_id)

        response = requests.get(self.__base_url + self.__method_get_sms, params=params)

        if "sms_code" in response.json():
            return response.json()['sms_code']
        else:
            raise SMSnotReceivedError(response.json()['error_msg'])

    def get_all_countries(self):
        """
        Return information about all countries

        :return: JSON of all countries with ID, name
        :rtype: json
        """

        response = requests.get(self.__base_url + self.__method_get_all_countries, params=self.__params)

        if "1" in response.json():
            return response.json()
        else:
            raise WrongTokenError(response.json()['error_msg'])

    def get_all_services(self):
        """
        Return information about all applications

        :return: JSON of all applications with ID, name
        :rtype: json
        """

        response = requests.get(self.__base_url + self.__method_get_all_services, params=self.__params)

        if "1" in response.json():
            return response.json()
        else:
            raise WrongTokenError(response.json()['error_msg'])

    def __check_params(self, country_id=None, application_id=None, request_id=None):
        """
        Create params for request

        :param country_id:
        :param application_id:
        :param request_id:
        :return: params
        :rtype: dict
        """

        params = self.__params

        if country_id:
            params['country_id'] = country_id
        if application_id:
            params['application_id'] = application_id
        if request_id:
            params['request_id'] = request_id

        return params
