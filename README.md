# SMSMAN Public API Python
[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a lightweight library that works as a connector to [Sms-Man public API](https://sms-man.com/site/docs-apiv2)  
## Installation

```bash
pip install smsman
```
## Documentation  
[https://sms-man.com/site/docs-apiv2](https://sms-man.com/site/docs-apiv2)
## RESTful APIs
Usage examples:
```python
from smsman.smsman import Smsman

api_key = ""

client = Smsman(api_key)

#  Get current balance
print(client.get_balance())

#  Get information about all services
print(client.get_all_services())

#  Get information about all countries
print(client.get_all_countries())

#  Get the number of numbers for the selected country and service
print(client.get_limits(country_id=1, application_id=1))

#  Buy new number
request_id, phone_number = client.request_phone_number(country_id=1,
                                                       application_id=1)

#  Receive a SMS to the number
sms_code = client.get_sms(request_id)

```
## Referral program
Detailed conditions of the affiliate program:

1. The referral program was created exclusively to stimulate and the dissemination of information about the sms-man.com
2. Each registered user sms-man.com can take part in the referral program.
3. The number of invited users by one user - unlimited
4. The inviting user is called the referrer, and the invited user is called the referral
5. The referrer who invited a new active referral receives 3% of the costs of the referral
6. The maximum amount of referral deductions from one referral is limited to $10. Upon reaching this amount accruals are suspended.
7. Referral funds are withdrawn within 24 hours of the application. The minimum withdrawal amount is $5. Transfer to [sms-man.com](https://sms-man.com) account is carried out instantly and without commission.
8. The sms-man.com administration has the right to refuse to pay funds if facts of fake up invited users or other cases of abuse of the referral program are established.  
  
## How do I use the referral program in the API?
Find your referral code [here](https://sms-man.com/site/profile)
```python
from smsman.smsman import Smsman

api_key = ""
ref_code = ""

client = Smsman(api_key, ref_code)
```
## Contributing

Contributions are welcome.<br/>
If you've found a bug within this project, please open an issue to discuss what you would like to change.<br/>
If it's an issue with the API, please write it on out site [Sms-man Feedback](https://sms-man.com/site/feedback)
