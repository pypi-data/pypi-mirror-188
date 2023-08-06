# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jito_geyser', 'jito_geyser.generated']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.51.1,<2.0.0', 'isort>=5.11.4,<6.0.0', 'protobuf>=4.21.12,<5.0.0']

setup_kwargs = {
    'name': 'jito-geyser',
    'version': '0.0.1',
    'description': 'Jito Labs Geyser Client',
    'long_description': '# About\nThis library contains python code to interact with [Jito\'s Geyser Plugin](https://github.com/jito-foundation/geyser-grpc-plugin).\n\n# Downloading\n```bash\n$ pip install jito_geyser\n```\n\n# Access Token\nPlease request access to geyser by emailing support@jito.wtf\n\n# Examples\n\n### Printing slot updates\n```python\nfrom grpc import ssl_channel_credentials, secure_channel\n\nfrom jito_geyser.generated.geyser_pb2 import SubscribeSlotUpdateRequest\nfrom jito_geyser.generated.geyser_pb2_grpc import GeyserStub\n\nGEYSER_URL = "mainnet.rpc.jito.wtf"\nACCESS_TOKEN = "ACCESS_TOKEN_HERE"\n\nchannel = secure_channel(GEYSER_URL, ssl_channel_credentials())\nclient = GeyserStub(channel)\nfor msg in client.SubscribeSlotUpdates(SubscribeSlotUpdateRequest(), metadata=[("access-token", ACCESS_TOKEN)]):\n    print(msg)\n```\n\n### Listening to program account updates\nThis example listens to pyth-owned accounts\n```python\nfrom grpc import ssl_channel_credentials, secure_channel\nfrom solders.pubkey import Pubkey # note: probably need to install solders for this import\n\nfrom jito_geyser.generated.geyser_pb2 import SubscribeProgramsUpdatesRequest\nfrom jito_geyser.generated.geyser_pb2_grpc import GeyserStub\n\nGEYSER_URL = "mainnet.rpc.jito.wtf"\nACCESS_TOKEN = "ACCESS_TOKEN_HERE"\nACCOUNTS = [bytes(Pubkey.from_string("FsJ3A3u2vn5cTVofAjvy6y5kwABJAqYWpe4975bi2epH"))]\n\nchannel = secure_channel(GEYSER_URL, ssl_channel_credentials())\nclient = GeyserStub(channel)\nfor msg in client.SubscribeProgramUpdates(SubscribeProgramsUpdatesRequest(programs=ACCOUNTS), metadata=[("access-token", ACCESS_TOKEN)]):\n    print(msg)\n```\n\n### Functions available\n- There are many functions available including:\n  - GetHeartbeatInterval\n  - SubscribeAccountUpdates\n  - SubscribeProgramUpdates\n  - SubscribePartialAccountUpdates\n  - SubscribeSlotUpdates\n  - SubscribeTransactionUpdates\n  - SubscribeBlockUpdates\n\n# Development\n\nInstall pip\n```bash\n$ curl -sSL https://bootstrap.pypa.io/get-pip.py | python 3 -\n```\n\nInstall poetry\n```bash\n$ curl -sSL https://install.python-poetry.org | python3 -\n```\n\nSetup environment and build protobufs\n```bash\n$ poetry install\n$ poetry shell\n$ poetry protoc\n```\n\nLinting\n```bash\n$ poetry run black .\n$ poetry run isort .\n```\n\nPublishing package\n```bash\n$ poetry protoc && poetry build && poetry publish\n```\n',
    'author': 'Jito Labs',
    'author_email': 'support@jito.wtf',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
