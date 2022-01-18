# import asyncio
#
# import aiohttp
import requests
from smsman.errors import WrongTokenError, SMSnotReceivedError, LowBalance, NoNumbers


class Smsman:
    __base_url = "http://api.sms-man.ru/control"
    __method_balance = "/get-balance"
    __method_get_limits = "/limits"
    __method_get_number = "/get-number"
    __method_get_sms = "/get-sms"
    __method_get_all_countries = "/countries"
    __method_get_all_services = "/applications"
    __method_reject_number = "/set-status"

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
        try:

            if "balance" in response.json():
                return float(response.json()['balance'])
            else:
                raise WrongTokenError(response.json()['error_msg'])
        except:
            self.get_balance()

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

        params['ref'] = self.__ref

        response = requests.get(self.__base_url + self.__method_get_number, params=params)
        resp_json = response.json()
        if "request_id" in resp_json and "number" in resp_json:
            return resp_json['request_id'], resp_json["number"]
        elif resp_json['error_code'] == "balance":
            raise LowBalance(resp_json['error_msg'])
        elif resp_json["error_code"] == "no_numbers":
            raise NoNumbers(resp_json["error_msg"])
        else:
            raise WrongTokenError(resp_json['error_msg'])

    # async def get_numbers(self, params, requests_id, numbers,
    #                       flag_balance, flag_numbers):
    #
    #     async with aiohttp.ClientSession() as session:
    #         response = await session.post(self.__base_url + self.__method_get_number, params=params)
    #         resp_json = await response.json()
    #         if "request_id" in resp_json and "number" in resp_json:
    #             requests_id.append(resp_json['request_id'])
    #             numbers.append(resp_json['number'])
    #         elif resp_json['error_code'] == "balance":
    #             flag_balance[0] += 1
    #         elif resp_json['error_code'] == "no_numbers":
    #             flag_numbers[0] += 1
    #
    # async def request_phone_numbers(self, country_id: str, application_id: str, amount):
    #     """
    #     Queries the phone number by country id and service id.
    #     Returns request number (needed to receive sms) and phone number.
    #
    #     :param country_id: id of country. Can check list on web-site or with method get_all_countries
    #     :param application_id: id of application. Can check list on web-site or with method get_all_services
    #     :param amount: Amount of numbers. No more than 100
    #     :return: requests_id, numbers
    #     :rtype: list, list
    #     """
    #
    #     tasks = []
    #     requests_id = []
    #     numbers = []
    #     flag_balance = [0]
    #     flag_numbers = [0]
    #
    #     params = self.__check_params(country_id, application_id)
    #     params['ref'] = self.__ref
    #
    #     for i in range(amount):
    #         task = asyncio.create_task(self.get_numbers(params, requests_id, numbers, flag_balance, flag_numbers))
    #         tasks.append(task)
    #     await asyncio.gather(*tasks)
    #     if len(requests_id) != 0:
    #         return requests_id, numbers
    #     elif flag_balance[0] == amount:
    #         raise LowBalance("No balance")
    #     elif flag_numbers[0] == amount:
    #         raise NoNumbers("No numbers")

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

    # async def change_status(self, request_id):
    #     params = {"token": self.__token,
    #               "request_id": request_id,
    #               "status": "reject"}
    #
    #     async with aiohttp.ClientSession() as session:
    #         await session.post(self.__base_url + self.__method_reject_number, params=params)
    #
    # async def reject_numbers(self, requests_id):
    #     tasks = []
    #
    #     for request_id in requests_id:
    #         task = asyncio.create_task(self.change_status(request_id))
    #         tasks.append(task)
    #
    #     await asyncio.gather(*tasks)

    def reject_number(self, request_id: str):
        """
        Returns the number if it did not receive an SMS. Money is returned to the balance
        :param request_id: Number of IF (get with phone number)
        """
        params = self.__check_params(request_id=request_id, status="reject")

        requests.get(self.__base_url + self.__method_reject_number, params=params)

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

    def __check_params(self, country_id=None, application_id=None, request_id=None, status=None):
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
        if status:
            params['status'] = status
        if request_id:
            params['request_id'] = request_id

        return params

