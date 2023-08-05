# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['dnspython>=2.2.1,<3.0.0',
 'impacket>=0.10.0,<0.11.0',
 'ldap3>=2.9,<3.0',
 'pycryptodomex>=3.15.0,<4.0.0']

entry_points = \
{'console_scripts': ['hekatomb = src.hekatomb:main']}

setup_kwargs = {
    'name': 'hekatomb',
    'version': '1.5',
    'description': 'Python library to extract and decrypt all credentials from all domain computers',
    'long_description': '# The HEKATOMB project\n\n<div align="center">\n  <br>\n  <img src="https://img.shields.io/badge/Python-3.6+-informational">\n  <br>\n  <a href="https://twitter.com/intent/follow?screen_name=ProcessusT" title="Follow"><img src="https://img.shields.io/twitter/follow/ProcessusT?label=ProcessusT&style=social"></a>\n  <br>\n  <h1>\n    Because Domain Admin rights are not enough.<br />\n                Hack them all.<br />\n                🐍\n  </h1>\n  <br><br>\n</div>\n\n> Hekatomb is a python script that connects to LDAP directory to retrieve all computers and users informations.<br />\n> Then it will download all DPAPI blob of all users from all computers.<br />\n>\tFinally, it will extract domain controller private key through RPC uses it to decrypt all credentials.<br />\n> <br />\n> \n<br>\n<div align="center">\n<img src="https://github.com/Processus-Thief/HEKATOMB/raw/main/.assets/hekatomb_v1.4.png" width="80%;">\n</div>\n<br>\n\n\n## Changelog\n<br />\nOn last version (V 1.4) :<br />\n- Fix LDAP search limitation to 1000 items<br />\n- Add LDAP filter for computers to select only "Enabled" computers<br />\n- Add function to scan SMB port with multi thread prior to get blob and master key files<br />\n- Add a progress bar for files collection<br />\n- Added 2 function modules to simplify code readability and maintainability<br />\n<br />\nV 1.3 :<br />\n- Compare LDAP usernames with SMB users folders before trying to retrieve blob files to get them faster<br />\n- DNSTCP option is no more used, DNS resolution is trying on UDP first and with TCP if it fails<br />\n<br />\nV 1.2.1 :<br />\n- Use of the ldap3 library instead of Impacket for LDAP requests<br />\n- Fix a bug that prevented querying trusted domains via an external domain account with administrator rights on the trusted domain controller<br />\n- Add -smb2 parameter to force the use of SMBv2 protocol when it is available<br />\n- LDAP and SMB communications are now more difficult to detect on the network<br />\n<br />\nV 1.2.1 :<br />\n- Add installation with Pypi<br />\n<br />\nV 1.2 :<br />\n- Increase the LDAP results limit of users or computers extraction (1000 previously)<br />\n- Add the possibility to specify a user or a computer to target<br />\n- Add the possibility to export results to a CSV file<br />\n<br />\nV 1.1 :<br />\n- Domain controller private key extraction through RPC<br />\n- Credentials classification by computers and by users<br />\n\n<br /><br />\n\n## What da fuck is this ?\n<br />\nOn Windows, credentials saved in the Windows Credentials Manager are encrypted using Microsoft\'s Data Protection API and stored as "blob" files in user AppData folder.<br />\nOutside of a domain, the user\'s password hash is used to encrypt these "blobs".<br />\nWhen you are in an Active Directory environment, the Data Protection API uses the domain controller\'s public key to encrypt these blobs.<br />\nWith the extracted private key of the domain controller, it is possible to decrypt all the blobs, and therefore to recover all the secrets recorded in the Windows identification manager of all the workstations in the domain.<br />\n<br />\nHekatomb automates the search for blobs and the decryption to recover all domain users\' secrets ☠️\n<br />\n<br />\n\n## Installation\n<br>\nFrom Pypi :\n<br><br>\n\n```python\npip3 install hekatomb\n```\n\n<br>\nFrom sources :\n<br><br>\n\n```python\ngit clone https://github.com/Processus-Thief/HEKATOMB\ncd HEKATOMB\npython3 setup.py install\n```\n\n<br><br>\n\n\n## Usage\n<br>\nHekatomb uses Impacket syntax :\n<br><br>\n\n```python\nusage: hekatomb [-h] [-hashes LMHASH:NTHASH] [-pvk PVK] [-dns DNS] [-dnstcp] [-port [port]] [-just-user JUST_USER] [-just-computer JUST_COMPUTER] [-md5] [-debug] [-debugmax] target\n\nScript used to automate domain computers and users extraction from LDAP and extraction of domain controller private key through RPC to collect and decrypt all users\' DPAPI secrets saved in Windows credential manager.\n\npositional arguments:\n  target                [[domain/]username[:password]@]<targetName or address of DC>\n\noptions:\n  -h, --help            Show this help message and exit\n\nauthentication:\n  -hashes LMHASH:NTHASH     NTLM hashes, format is LMHASH:NTHASH\n\nauthentication:\n  -pvk PVK                  Domain backup keys file\n  -dns DNS                  DNS server IP address to resolve computers hostname\n  -port [port]              Port to connect to SMB Server\n  -smb2                     Force the use of SMBv2 protocol\n  -just-user [USERNAME]     Test only specified username\n  -just-computer [COMPUTER] Test only specified computer\n  -md5                      Print md5 hash insted of clear passwords\n\nverbosity:\n  -debug                Turn DEBUG output ON\n  -debugmax             Turn DEBUG output TO MAAAAXXXX\n```\n\n<br>\n<br>\n\n## Example\n\n<br>\n\n```python\nhekatomb -hashes :ed0052e5a66b1c8e942cc9481a50d56 DOMAIN.local/administrator@10.0.0.1 -debug \n```\n\n<br>\n<br>\n    \n## How to retrieve domain backup keys ?\n\n<br />\nIf no domain backup keys are provided, the script will retrieve it through RPC\n',
    'author': 'Processus Thief',
    'author_email': 'hekatomb@thiefin.fr',
    'maintainer': 'Processus Thief',
    'maintainer_email': 'hekatomb@thiefin.fr',
    'url': 'https://github.com/Processus-Thief/HEKATOMB',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
