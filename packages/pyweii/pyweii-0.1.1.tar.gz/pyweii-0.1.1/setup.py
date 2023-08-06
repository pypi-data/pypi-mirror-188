# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyweii']

package_data = \
{'': ['*']}

install_requires = \
['evdev>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['weii = pyweii.cli:cli']}

setup_kwargs = {
    'name': 'pyweii',
    'version': '0.1.1',
    'description': 'A utility to measure weight using the Wii Balance Board.',
    'long_description': 'Weii\n====\n\nWeii (pronounced "weigh") is a small script that connects to a Wii Balance Board, reads a weight measurement, and disconnects.\nWeii is the new, redesigned spiritual successor to [gr8w8upd8m8](https://github.com/skorokithakis/gr8w8upd8m8).\n\nInstallation\n------------\n\nTo install using `pipx` (recommended) or `pip`, run:\n\n```\npipx install pyweii\n```\n\nor\n\n```\npip install pyweii\n```\n\n\nUsage\n-----\n\nWeii currently is only tested on Linux.\nBefore you use Weii, you need to pair your balance board via Bluetooth.\nYou can do that by pressing the red button in the battery compartment and then going through the normal Bluetooth pairing process.\nI don\'t remember the pairing code, try 0000 or 1234, and please let me know which one is right.\n\nTo weigh yourself, run `weii` and follow the instructions.\nYou need to have paired your balance board beforehand, then press the button at the front of the board until the blue LED lights up solid, and step on.\nOnce the measurement is done, you can step off.\n\nWeii can optionally use `bluetoothctl` to disconnect (and turn off) the balance board when the weighing is done, you can do that by passing the device\'s address to the `-d` argument:\n\n```\nweii --disconnect-when-done 11:22:33:44:55:66\n```\n\nYou can run a command after weighing, like so:\n\n```\nweii --command "echo {weight}"\n```\n\n`{weight}` will be replaced with the measured weight.\n\nYou can also adjust the measurement to account for clothing, or to match some other scale:\n\n```\nweii --adjust=-2.3\n```\n\nChangelog\n=========\n\n\n(unreleased)\n------------\n\nFix\n~~~\n- Rename `terse` argument. [Stavros Korokithakis]\n\nOther\n~~~~~\n- Build: Release v0.1.1. [Stavros Korokithakis]\n- Doc: Documentation updates. [Stavros Korokithakis]\n- Switch to ruff. [Stavros Korokithakis]\n- Chore: Add repository and homepage. [Stavros Korokithakis]\n- Feat: Abort if the user presses the board button while measuring.\n  [Stavros Korokithakis]\n- Feat: Add the `--command` argument. [Stavros Korokithakis]\n- Add LICENSE. [Stavros Korokithakis]\n- Doc: Add changelog. [Stavros Korokithakis]\n- Initial commit. [Stavros Korokithakis]\n\n\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/stavros/weii',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
