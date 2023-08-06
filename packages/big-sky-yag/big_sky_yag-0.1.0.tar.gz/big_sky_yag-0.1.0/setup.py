# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['big_sky_yag']

package_data = \
{'': ['*']}

install_requires = \
['PyVISA>=1.12.0,<2.0.0']

setup_kwargs = {
    'name': 'big-sky-yag',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Big-Sky-YAG\n Python interface for a Big Sky YAG Laser.\n\n## Example\n```Python\nfrom big_sky_yag import BigSkyYag\n\nresource_name = "COM4"\n\nyag = BigSkyYag(resource_name = resource_name)\n\n# print the status of the laser\nprint(yag.laser_status())\n\n# set the flashlamp frequency\nyag.flashlamp.frequency = 10 # Hz\n\n# set the flashlamp voltage\nyag.flashlamp.voltage = 900 # V\n\n# set the q-switch delay\nyag.qswitch.delay = 150 # ns\n\n# start the water pump\nyag.pump = True\n\n# open the shutter, activate the flashlamp and enable the q-switch\nyag.shutter = True\nyag.flashlamp.activate()\nyag.qswitch.start()\n\n# stop the yag from firing\nyag.qswitch.stop()\nyag.flashlamp.stop()\n```\n\n## Change Firing Mode\nThe flashlamp and Q-Switch can be triggered either internally, externally, or in case of the Q-switch also in burst mode.\n### Flashlamp\n* internal trigger \n  ``` Python\n  yag.flashlamp.trigger = "internal"\n  ```\n* external trigger\n    ``` Python\n  yag.flashlamp.trigger = "external"\n  ```\n\n### Q-Switch\n* internal\n  ```Python\n  yag.qswitch.mode = "auto"\n  ```\n* burst\n  ```Python\n  yag.qswitch.pulses = 10 # nr. pulses in burst mode\n  yag.qswitch.mode = "burst"\n  ```\n* external\n  ```Python\n  yag.qswitch.mode = "external"\n  ```\n\n### Other commands\n* save the current configuration\n  ```Python\n  yag.save()\n  ```\n* retrieve the serial number\n  ```Python\n  yag.serial_number\n  ```\n* flashlamp counter\n  ```Python\n  yag.flashlamp.counter\n  ```\n* flashlamp user counter\n  ```Python\n  yag.flashlamp.user_counter\n  yag.flashlamp.user_counter_reset()\n  ```\n* q-switch counter\n  ```Python\n  yag.flashlamp.counter\n  ```\n* q-switch user counter\n  ```Python\n  yag.qswitch.counter_user\n  yag.qswitch.counter_user()\n  ```\n* nr. pulses to wait before starting the q-switch\n  ```Python\n  yag.qswitch.pulses_wait\n  ```\n* single q-switch shot\n  ```Python\n  yag.qswitch.single()\n  ```',
    'author': 'ograsdijk',
    'author_email': 'o.grasdijk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ograsdijk/Big-Sky-YAG',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
