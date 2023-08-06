# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['daraja_connect', 'test']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'daraja-connect',
    'version': '0.1.0b2',
    'description': 'A wrapper library for the Daraja Mpesa API',
    'long_description': '# DARAJA CONNECT\n\nA wrapper library for the Daraja Mpesa API\n\n[![Language](https://img.shields.io/badge/language-python-green.svg)](https://python.org)\n\n## Features\n\n- Authorization\n- Mpesa Express\n  - STK Push\n  - Query\n- Customer To Business (C2B)\n    - Register URL\n    - Simulate\n- Business To Customer (B2C)\n- Account Balance\n- Transaction Status\n\n## Installation\n\n    $ pip install daraja-connect\n\n## Usage\n\n*NOTE: Before you start, make sure to go through the official Daraja Mpesa API [documentation](https://developer.safaricom.co.ke/Documentation)* \n\nCreate an app instance. \n\n```python\nfrom daraja_connect import App\n\n# Sandbox\napp = App.create_sandbox(consumer_key=..., consumer_secret=...)\n\n# Production\napp = App.create_production(consumer_key=..., consumer_secret=...)\n```\n\nGenerate an authorization token.\n\n```python\nfrom daraja_connect import Authorization\n\nauth = Authorization(app)\nresult = auth.generate_token()\naccess_token = result.access_token\n```\n*You can attach this token to the service instance or include it as an argument to the api methods calls*\n\n### Mpesa Express\n\n**STK Push**\n```python\nfrom daraja_connect import STKPush\n\nstk = STKPush(app, access_token=access_token)\nresult = stk.process_request(\n    business_short_code=...,\n    phone_number=...,\n    amount=...,\n    call_back_url=...,\n    account_reference=...,\n    transaction_desc=...,\n    password=...,\n    timestamp=...,\n)\n```\n\n**Query**\n```python\nresult = stk.query(\n    business_short_code=...,\n    checkout_request_id=...,\n    password=...,\n)\n```\nYou can use the `generate_password` helper to create a password\n\n```python\nfrom daraja_connect.utils import generate_password\n\npassword = generate_password(\n    business_short_code=....,\n    pass_key=...,\n    timestamp=...,\n)\n```\nAlternatively, you can include the `pass_key` argument in place of `password` to auto generate the password\n\n### Customer To Business (C2B) API\n\n**Register URL**\n```python\nfrom daraja_connect import C2B\nfrom daraja_connect.enums import ResponseType\n\nc2b = C2B(app, access_token=access_token)\nresult = c2b.register_url(\n    short_code=...,\n    validation_url=...,\n    confirmation_url=...,\n    response_type=ResponseType.COMPLETED,\n)\n```\n\n**Simulate**\n```python\nresult = c2b.simulate(\n    short_code=...,\n    command_id=TransactionType.CUSTOMER_PAY_BILL_ONLINE,\n    amount=...,\n    msisdn=...,\n    bill_ref_number=...,\n)\n```\n\n### Business To Customer (B2C) API\n\n```python\nfrom daraja_connect import B2C\nfrom daraja_connect.enums import TransactionType\n\nb2c = B2C(app, access_token=access_token)\nresult = b2c.payment_request(\n    initiator_name=...,\n    security_credential=...,\n    amount=...,\n    command_id=TransactionType.BUSINESS_PAYMENT,\n    party_a=...,\n    party_b=...,\n    queue_time_out_url=...,\n    result_url=...,\n    remarks=...,\n    occassion=...,\n)\n```\n\n### Account Balance API\n\n```python\nfrom daraja_connect import AccountBalance\nfrom daraja_connect.enums import TransactionType, IdentifierType\n\nab = AccountBalance(app, access_token=access_token)\nresult = ab.query(\n    initiator=...,\n    security_credential=...,\n    command_id=TransactionType.ACCOUNT_BALANCE,\n    identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,\n    party_a=...,\n    queue_time_out_url=...,\n    result_url=...,\n    remarks=...,\n)\n```\n\n### Transaction Status API\n\n```python\nfrom daraja_connect import TransactionStatus\nfrom daraja_connect.enums import TransactionType, IdentifierType\n\nts = TransactionStatus(app, access_token=access_token)\nresult = ts.query(\n    initiator=...,\n    security_credential=...,\n    transaction_id=...,\n    command_id=TransactionType.TRANSACTION_STATUS_QUERY,\n    identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,\n    party_a=...,\n    queue_time_out_url=...,\n    result_url=...,\n    remarks=...,\n    occassion=...,\n)\n```\n\nAll API methods return a result object with a response property which is a [`requests.Response`](https://requests.readthedocs.io/en/latest/api/#requests.Response) object and various properties corresponding to the json body of the response\n\n## Running Tests\n\nInstall dependencies\n\n    $ poetry install\n\nCreate `.env` file from [.env.example](https://github.com/enwawerueli/daraja-connect/blob/main/.env.example) then edit it to add your app credentials and test parameters\n\n    $ cp .env.example .env\n\n Run tests\n\n    $ poetry run pytest\n\n## License\n\n[MIT](https://github.com/enwawerueli/daraja-connect/blob/main/LICENSE)\n',
    'author': 'Emz D',
    'author_email': 'seaworndrift@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/enwawerueli/daraja-connect',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
