import requests

import gopac

proxy = gopac.find_proxy('https://antizapret.prostovpn.org/proxy.pac', 'https://www.linkedin.com')
response = requests.get('https://www.linkedin.com', proxies=proxy)
print(response.text)
