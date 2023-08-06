# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mobizon_client']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

setup_kwargs = {
    'name': 'mobizon-client',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Mobizon Client\n\n#### [Ссылка на официальную документацию](https://mobizon.kz/help/api-docs/sms-api)\n\n## Примеры:\n\n### Асинхронный клиент\n\n```python\nimport asyncio\nfrom mobizon_client import AsyncMobizonClient\n\n\nasync def main():\n    url = 'https://api.mobizon.kz'\n    api_key = 'xisNSPPFj05WTVyH5oALU86VVuH7SocEUiitN0Og'\n    client = AsyncMobizonClient(url=url, api_key=api_key)\n    result = await client.send_message(recipient='77071234567', text='Test message', sender_signature=None)\n    await asyncio.sleep(3)\n    result = await client.get_message_status([result.message_id])\n    assert result[0].status == 'DELIVRD'\n    await client.close()\n\n\nif __name__ == '__main__':\n    asyncio.run(main())\n```\n\n### Синхронный клиент\n\n```python\nfrom time import sleep\nfrom mobizon_client import MobizonClient\n\n\ndef main():\n    url = 'https://api.mobizon.kz'\n    api_key = 'xisNSPPFj05WTVyH5oALU86VVuH7SocEUiitN0Og'\n    client = MobizonClient(url=url, api_key=api_key)\n    result = client.send_message(recipient='77071234567', text='Test message', sender_signature=None)\n    sleep(3)\n    result = client.get_message_status([result.message_id])\n    assert result[0].status == 'DELIVRD'\n    client.close()\n\n\nif __name__ == '__main__':\n    main()\n```",
    'author': 'Stanislav Tsoy',
    'author_email': 'dev.stanislav@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/devstsoy/mobizon-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
